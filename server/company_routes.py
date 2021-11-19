from flask import Blueprint, request, jsonify
from user_verification import verify_user
from database_connection import db_connection

company_api = Blueprint('company_api', __name__)

@company_api.route("/company/<company_id>", methods=["GET"])
def company(company_id):

    user_verification = verify_user(company_id)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET":
        conn = db_connection()
        cursor = conn.cursor()
        sql = f"""SELECT Company_id, Company_name FROM `Company` WHERE Company_id = {company_id}"""
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return jsonify(result)
        return {"errorCode": 404, "Message": "Company Does not exist"""}