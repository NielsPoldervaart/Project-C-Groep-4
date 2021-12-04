from flask import request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from user_verification import verify_user
from database_connection import *


login_api = Blueprint('login_api', __name__)

@login_api.route("/login", methods=["POST"])
def login():
    conn = db_connection()
    cursor = conn.cursor()

    db_session = create_db_session()

    if request.method == "POST":

        #JSON METHOD
        jsonInput = request.json
        inserted_password = jsonInput["password"]
        inserted_user_email = jsonInput["email"]

        user = db_session.query(User.user_id, User.Company_company_id, User.Role_role_id, User.password).filter_by(email =f'{inserted_user_email}').first()
        if user: #IF USER OBJECT IS NOT NONE (COULD FIND CORRECT DATA IN DB)
            if not check_password_hash(user.password, inserted_password):
                return {"Code": 406, "Message": "Incorrect User credentials (PASSWORD)"} #TODO: REMOVE "(PASSWORD)" FROM RESPONSE"

            session["user_id"] = user.user_id
            session["company_company_id"] = user.Company_company_id
            session["role_role_id"] = user.Role_role_id
            return {"Code": 201, "Message": "User logged in"}

        else:
           return {"Code": 406, "Message": "Incorrect User credentials (NAME)"} #TODO: REMOVE "(NAME) FROM RESPONSE"

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

        sql = f"""INSERT INTO `User` VALUES (default, "{inserted_first_name}", "{inserted_last_name}", "{inserted_user_email}", "{hashed_password}", "{company_id}", "{inserted_role}");"""
        cursor.execute(sql)
        conn.commit()

        return {"Code": 201, "Message": "User added to company"""}