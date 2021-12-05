from flask import Blueprint, request, jsonify
from user_verification import verify_user
from database_connection import *
import os

template_api = Blueprint('template_api', __name__)

@template_api.route("/templates/<company_identifier>", methods=["GET", "POST"])
def templates(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()

    if request.method == "GET": #View ALL templates from a company
        #SELECT `Template_id`, `Template_file`, Company_name WHERE `Company_1` = company_identifier
        result = db_session.query(Template.template_id, Template.template_file, Company.company_name).join(Company).filter_by(company_id = f'{company_identifier}').all()

        templates = [
            dict(
                template_id = row['template_id'],
              template_file = row['template_file'],
                company_name = row['company_name']
                )
                for row in result
        ]  
        if len(templates) is not 0:
            return jsonify(templates)
        else:
            return {"errorCode": 404, "Message": "Template Does not exist"""}

    if request.method == "POST": #Add a template to DB
        #TODO: ACTUAL TEMPLATE NEEDS TO BE ADDED TO STORAGE

        new_template_path = request.form["template_path"]
        #New Template object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_template = Template(None, new_template_path, company_identifier)

        db_session.add(new_template)
        db_session.commit()

        return {"Code": 201, "Message": "Template added to company"""}

@template_api.route("/template/<company_identifier>/<template_identifier>", methods=["GET", "DELETE"])
def template(company_identifier, template_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    conn = db_connection()
    cursor = conn.cursor()

    db_session = create_db_session()


    if request.method == "GET": #View a specific template

        result = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()

        if result is not None:
            return dict(
                template_id = result.template_id,
                template_file = result.template_file,
                Company_company_id = result.Company_company_id
            )
        return {"errorCode": 404, "Message": "Template Does not exist"""}

    if request.method == "Delete" : #Delete a specific template
        #sql = f"""Select template_file from Template where template_id = {template_id} and company_company_id = {company_id}
        #"""
        #sql2 = f"""Delete from Template where template_id = {template_id} and company_company_id = {company_id}
        #"""
        cursor.execute(sql)
        result = cursor.fetchone()
        path = result.get("template_file")
        os.remove(path)
        #cursor.execute(sql2)
        #conn.commit()
        return {"Code": 201, "Message": "Deleted file succesfully"""}