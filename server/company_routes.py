from flask import Blueprint, request, jsonify
from user_verification import verify_user
from database_connection import *

company_api = Blueprint('company_api', __name__)

@company_api.route("/company/<company_identifier>", methods=["GET"])
def company(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET":
        db_session = create_db_session()
        company_information = db_session.query(Company.company_id, Company.company_name).filter_by(company_id = company_identifier).first()

        if company_information is not None:
            return dict(
                company_id = company_information.company_id,
                company_name = company_information.company_name
            )
        return {"errorCode": 404, "Message": "Company Does not exist"""}, 404

@company_api.route("/<company_identifier>/accounts", methods=["GET", "POST"])
def company_accounts(company_identifier):

    user_verification = verify_user(company_identifier) #TODO: WHICH USERS ARE ALLOWED TO MAKE THIS REQUEST (SHOULD IT BE DIFFERENT FOR POST/GET)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET":
        db_session = create_db_session()
        users_dictionary = {}
        company_has_no_users = True
        verified_users_information = db_session.query(User.email, User.username, User.Role_role_id).filter_by(Company_company_id = company_identifier).filter_by(verified = True).all()
        awaiting_users_information = db_session.query(User.email, User.username, User.Role_role_id).filter_by(Company_company_id = company_identifier).filter_by(verified = False).all()

        if verified_users_information is not None:
            company_has_no_users = True
            users_dictionary["Verified_users"] =[
                dict(
                email = row["email"],
                username = row["username"],
                user_role = row["Role_role_id"]
                )
                for row in verified_users_information
            ]
        else:
            users_dictionary["Verified_users"] = []

        if awaiting_users_information is not None:
            company_has_no_users = True
            users_dictionary["Awaiting_users"] =[
                dict(
                email = row["email"],
                username = row["username"],
                user_role = row["Role_role_id"]
                )
                for row in awaiting_users_information
            ]
        else:
            users_dictionary["Awaiting_users"] = []
        
        if company_has_no_users:
            return {"errorCode": 404, "Message": "Company has no accounts"} , 404

        return users_dictionary, 200


    if request.method == "POST":
        form_user_id = request.form['user_id'] #STRING: WHICH USER TO BE ADDED / DECLINED
        form_accepted = request.form['accepted'] #BOOLEAN: WHETHER USER SHOULD BE ADDED TO COMPANY (APPROVED)
        db_session = create_db_session()
        extracted_user = db_session.query(User).filter_by(Company_company_id = company_identifier).filter_by(user_id = form_user_id).first()

        if extracted_user is None:
            return {"errorCode": 404, "Message": "User does not exist within company"} , 404

        if form_accepted:
            #change user to verified in DB
            extracted_user.verified = True
            db_session.commit()
            db_session.close()

            return {"returnCode": 201, "Message": "User's verified status updated"} , 201

        else:
            #remove user from DB
            db_session.delete(extracted_user)
            db_session.commit()
            db_session.close()
            return {"returnCode": 201, "Message": "User deleted from system"} , 201


    return {"errorCode": 500, "Message": "Internal server error"} , 500 #Something went wrong