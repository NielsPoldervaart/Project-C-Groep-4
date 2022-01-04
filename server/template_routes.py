from flask import Blueprint, request, send_file, session
from user_verification import verify_user
from ftp_controller import try_to_get_text_file_ftps, delete_file_ftps, upload_file
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

template_api = Blueprint('template_api', __name__)

@template_api.route("/templates/<company_identifier>", methods=["GET", "POST"])
def templates(company_identifier):

    db_session = create_db_session()

    if request.method == "GET": #View ALL templates from a company
        #SELECT `Template_id`, `Template_file`, Company_name WHERE `Company_1` = company_identifier

        user_verification = verify_user(company_identifier) #make sure user is logged in correctly
        if user_verification != "PASSED":
            return user_verification

        result = db_session.query(Template.template_id, Template.template_file, Company.company_name).join(Company).filter_by(company_id = f'{company_identifier}').all()

        templates = [
            dict(
                template_id = row['template_id'],
                template_file = row['template_file'],
                )
                for row in result
        ]
        if len(templates) != 0:
            Dict = {}
            Dict["company_name"] = result[0].company_name
            Dict["user_role"] = session["role_role_id"]
            Dict["templates"] = templates
            return Dict
        return {"errorCode": 404, "Message": "Template Does not exist"""}

    if request.method == "POST": #Add a template to specific company as KYNDA_ADMIN
        uploaded_template = request.files['template_file']
        if uploaded_template.filename == '': 
            return {"Code": 405, "Message": "No template file found in request, OR File has no valid name"}

        if not (uploaded_template.filename.endswith(".html") or uploaded_template.filename.endswith(".htm")):
            return  {"Code": 405, "Message": "No template file found in request, OR File has no valid extension (.html OR .htm)"}

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        uploaded_template.save(random_file_path) #Save template to created storage
        upload_file(random_file_path, f"{uploaded_template.filename}", "templates", company_identifier)

        os.remove(random_file_path)

        #New Template object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_template = Template(None, f"{uploaded_template.filename}", company_identifier)
        
        db_session.add(new_template)
        db_session.commit()

        return {"Code": 201, "Message": "Template added to company"}

@template_api.route("/template/<int:company_identifier>/<int:template_identifier>", methods=["GET", "DELETE"])
def template(company_identifier, template_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()

    if request.method == "GET": #Open specific template (to view or to create a product)
        #result = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
        template_file_location_ftp = db_session.query(Template.template_file).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()

        if template_file_location_ftp is not None:
            print(type(template_file_location_ftp.template_file), template_file_location_ftp.template_file)

            template_bytes = try_to_get_text_file_ftps(template_file_location_ftp.template_file, "templates", company_identifier)
            if template_bytes is dict: #Dict means something went wrong, the error code + message defined in try_to_get_text_file will be returned
                return template_bytes

            return send_file(template_bytes, mimetype="text/html")

        return {"errorCode": 404, "Message": "Template Does not exist"""}

    if request.method == "DELETE" : #Delete a specific template as KYNDA_ADMIN or COMPANY_ADMIN

    #TODO: FIND A WAY TO ACCESS THE TEMPLATE FILE WITH ONE QUERY FOR DELETION, INSTEAD OF HAVING TO QUERY TWICE (SPEED INCR, OPTIONAL)
        template_to_delete = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
        if template_to_delete is None:
            return {"Code": 404, "Message": "Template not found in database"}

        path = template_to_delete.template_file
        attempt_to_remove = delete_file_ftps(path, 'templates', company_identifier) #TODO: Change 'templates' to actual dynamic var (will not work with image files currently (can get type from file path[etc] and then set accordingly))
        #TODO: CHECK Value of attempt to remove is 201, if not, dont unlink from database (File is not removed from)
        db_session.delete(template_to_delete)
        db_session.commit()
        
        return attempt_to_remove



@template_api.route("/multiplefiles", methods = ["POST"])
def multiple_files():
    if request.method == "POST":
        uploaded_files = request.files.getlist('Files')

        for file in uploaded_files:
            random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
            if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
                random_file_path = generate_random_path(24, 'html')

            file.save(random_file_path) #Save template to created storage
            upload_file(random_file_path, f"{file.filename}", "multiplefiles", 1)

            os.remove(random_file_path)
    
    return {}