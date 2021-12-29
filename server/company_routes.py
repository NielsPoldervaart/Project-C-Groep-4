from flask import Blueprint, request, send_file, current_app
from user_verification import verify_user
from database_connection import *
from ftp_controller import try_to_get_text_file_ftps, generate_random_path, upload_file
import os
from os import path

company_api = Blueprint('company_api', __name__)

@company_api.route("/company/<company_identifier>", methods=["GET"])
def company(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET":
        with create_db_session(current_app.config["DATABASE_URI"]) as db_session:
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
        users_dictionary = {}
        company_has_no_users = True

        with create_db_session(current_app.config["DATABASE_URI"]) as db_session:
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
        with create_db_session(current_app.config["DATABASE_URI"]) as db_session:
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


@company_api.route("/<company_identifier>/manual", methods=["GET", "POST"])
def company_manual(company_identifier):
    
    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET": #Open specific manual (to view)
        with create_db_session(current_app.config["DATABASE_URI"]) as db_session:
            #result = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
            manual_file_location_ftp = db_session.query(Manual.template_file).filter_by(Company_company_id = company_identifier).first()

        if manual_file_location_ftp is not None:
            manual_bytes = try_to_get_text_file_ftps(manual_file_location_ftp, "manual", company_identifier)
            if manual_bytes is dict: #Dict means something went wrong, the error code + message defined in try_to_get_text_file will be returned
                return manual_bytes

            return send_file(manual_bytes, mimetype="text/html")

        return {"errorCode": 404, "Message": "Manual Does not exist"""}

    if request.method == "POST": #Upload a manual to Company
        uploaded_template = request.files['template_file']
        if uploaded_template.filename == '': 
            return {"Code": 405, "Message": "No manual file found in request, OR File has no valid name"}

        if not (uploaded_template.filename.endswith(".html") or uploaded_template.filename.endswith(".htm")):
            return  {"Code": 405, "Message": "No manual file found in request, OR File has no valid extension (.html OR .htm)"}

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        uploaded_template.save(random_file_path) #Save template to created storage
        upload_file(random_file_path, f"{uploaded_template.filename}", "manual", company_identifier)

        os.remove(random_file_path)

        #New Template object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_template = Template(None, f"{uploaded_template.filename}", company_identifier)
        with create_db_session(current_app.config["DATABASE_URI"]) as db_session:
            db_session.add(new_template)
            db_session.commit()

        return {"Code": 201, "Message": "Manual added to company"}

@company_api.route("/", methods=["GET"])
def index():
    return {}
