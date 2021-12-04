from flask import request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from user_verification import verify_user
from database_connection import *


login_api = Blueprint('login_api', __name__)

@login_api.route("/login", methods=["POST"])
def login():
    conn = db_connection()
    cursor = conn.cursor()

    connSQLA = loadSession()

    if request.method == "POST": #haal wachwoord van server voor juiste user

        #JSON METHOD
        jsonInput = request.json
        inserted_password = jsonInput["password"]
        inserted_user_email = jsonInput["email"]

        sql = f"""Select user_id, company_company_id, role_role_id, password from User where email = "{inserted_user_email}" """
        cursor.execute(sql)
        user = cursor.fetchone()

        if user: #IF USER OBJECT IS NOT NONE (COULD FIND CORRECT DATA IN DB)
            if not check_password_hash(user["password"], inserted_password):
                return {"Code": 406, "Message": "Incorrect User credentials (PASSWORD)"}

            session["user_id"] = user["user_id"]
            session["company_company_id"] = user["company_company_id"]
            session["role_role_id"] = user["role_role_id"]
            return {"Code": 201, "Message": "User logged in"}

        else:
           return {"Code": 406, "Message": "Incorrect User credentials (NAME)"}

@login_api.route("/logout", methods = ["GET"])
def logout():
    if request.method == "GET":
        session.pop("user_id", None)
        session.pop("company_company_id", None)
        session.pop("role_role_id", None)
        return {"Code": 201, "Message": "User logged out"""}

@login_api.route("/register/<company_id>", methods = ["POST"])
def register(company_id):
    #TODO: COMPANY ID CAN BE RETRIEVED FROM USER DATA IN SESSION
    user_verification = verify_user(company_id, [1])
    if user_verification != "PASSED":
        return user_verification

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        inserted_first_name = request.form["first_name"]
        inserted_last_name = request.form["last_name"]
        inserted_user_email = request.form["email"]
        inserted_password = request.form["password"]
        inserted_role = request.form["role_id"]
        hashed_password = generate_password_hash(inserted_password)
        print("HASHED PASSWORD: " + hashed_password)

        sql = f"""INSERT INTO `User` VALUES (default, "{inserted_first_name}", "{inserted_last_name}", "{inserted_user_email}", "{hashed_password}", "{company_id}", "{inserted_role}");"""
        cursor.execute(sql)
        conn.commit()

        return {"Code": 201, "Message": "User added to company"""}