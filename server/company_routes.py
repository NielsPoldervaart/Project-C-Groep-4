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
        return {"errorCode": 404, "Message": "Company Does not exist"""}