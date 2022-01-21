from flask import request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from database_connection import *


login_api = Blueprint('login_api', __name__)

@login_api.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST": #LOGIN TO THE SERVER
        jsonInput = request.json
        inserted_username = jsonInput["name"]
        inserted_password = jsonInput["password"]

        with create_db_session() as db_session:
            #REQUESTS `user_id`, `Company_company_id`, `Role_role_id`, `password` FROM DATABASE WHERE EMAIL IS INSERTED EMAIL. RETURNS NONE IF CANNOT FIND MATCH
            user = db_session.query(User.user_id, User.Company_company_id, User.Role_role_id, User.password, User.email).filter_by(username =f'{inserted_username}').first()

        if user is None: #IF USER OBJECT IS NOT NONE (COULD FIND CORRECT DATA IN DB)
            return {"Code": 406, "Message": "Incorrect User credentials"}, 406 

        if not check_password_hash(user.password, inserted_password):
            return {"Code": 406, "Message": "Incorrect User credentials"}, 406

        #SET FLASK SESSION DATA TO USER CREDENTIALS
        session["user_id"] = user.user_id 
        session["company_company_id"] = user.Company_company_id
        session["role_role_id"] = user.Role_role_id
        return {"Code": 200, "Message": "User logged in"}, 200


    if request.method == "GET": #RETRIEVE FLASK SESSION DATA FROM LOGIN USER
        try:
            returnDict = {}
            returnDict["user_id"] = session["user_id"]
            returnDict["company_company_id"] = session["company_company_id"]
            returnDict["role_role_id"] = session["role_role_id"]
            if returnDict is not None:
                return returnDict
            return {"Code": 404, "Message": "Session data not found"}, 404
        except:
            return {"Code": 500, "Message": "Internal server error (Session)"}, 500


@login_api.route("/logout", methods = ["GET"])
def logout():
    if request.method == "GET": #LOGOUT OF SERVER
        session.pop("user_id", None) #None is the return value after popping
        session.pop("company_company_id", None)
        session.pop("role_role_id", None)
        return {"Code": 201, "Message": "User logged out"""}, 201

@login_api.route("/register/<int:company_identifier>", methods = ["POST"])
def register(company_identifier):
    if request.method == "POST": #SEND A REQUEST FOR A NEW ACCOUNT
        requested_username = request.form["name"]
        requested_user_email = request.form["email"]
        requested_password = request.form["password"]
        requested_role = request.form["role_id"]

        with create_db_session() as db_session:
            requested_company = db_session.query(Company.company_id).filter_by(company_id = company_identifier).first()
            #Verify if requested company exists within DB
            if requested_company is None:
                return {"Code": 404, "Message": "Requested company does not exist"}, 404

            new_user = User(None, requested_username, generate_password_hash(requested_user_email), generate_password_hash(requested_password), False, company_identifier, requested_role)
            db_session.add(new_user)
            db_session.commit()

        return {"Code": 201, "Message": "User added to company"}, 201