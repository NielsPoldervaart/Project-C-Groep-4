from flask import Blueprint, request, jsonify, send_from_directory
from user_verification import verify_user
from ftptest import get_file_full
from database_connection import *

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

@template_api.route("/template/<int:company_identifier>/<int:template_identifier>", methods=["GET", "DELETE"])
def template(company_identifier, template_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()

    if request.method == "GET": #View a specific template

        #result = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
        template_file_location_ftp = db_session.query(Template.template_file).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()

        if template_file_location_ftp is not None:
            print(type(template_file_location_ftp.template_file), template_file_location_ftp.template_file)
            get_file_full(template_file_location_ftp.template_file, company_identifier)
            try:
                return send_from_directory("database/templates/", template_file_location_ftp.template_file, as_attachment=True)
            except:
                return "NOPE"
            #download file from ftp
            #return file to client
            #delete file from local storage

        #if result is not None:
        #    return dict(
        #        template_id = result.template_id,
        #        template_file = result.template_file,
        #        Company_company_id = result.Company_company_id
        #    )
        return {"errorCode": 404, "Message": "Template Does not exist"""}

    if request.method == "DELETE" : #Delete a specific template

        #TODO: FIND A WAY TO ACCESS THE TEMPLATE FILE WITH ONE QUERY FOR DELETION, INSTEAD OF HAVING TO QUERY TWICE (SPEED INCR, OPTIONAL)
        template_to_delete = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
        #TODO: ADD CHECK IF TEMPLATE_TO_DELETE = NONE (NO TEMPLATE COULD BE FOUND WITH PROVIDED REQUIRMEMENTS, RETURN CORRECT DATA THEN)
        path = template_to_delete.template_file
        db_session.delete(template_to_delete)
        db_session.commit()

        path = template_to_delete.template_file
        print(path)
        #os.remove(path) TODO: ADD CONNECTION TO ACTUAL STORAGE TO DELETE THE TEMPLATE THERE WITH THE GATHERED PATH

        return {"Code": 201, "Message": "Deleted file succesfully"""}