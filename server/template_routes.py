from flask import Blueprint, request, send_file, session
from user_verification import verify_user
from ftp_controller import try_to_get_file_ftps_binary, try_to_delete_file_ftps, try_to_upload_file_ftps
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

template_api = Blueprint('template_api', __name__)

@template_api.route("/templates/<int:company_identifier>", methods=["GET", "POST"])
def templates(company_identifier):

    if request.method == "GET": #View ALL templates from a company
        #SELECT `Template_id`, `Template_file`, Company_name WHERE `Company_1` = company_identifier

        user_verification = verify_user(company_identifier) #make sure user is logged in correctly
        if user_verification != "PASSED":
            return user_verification

        with create_db_session() as db_session:
            result = db_session.query(Template.template_id, Template.template_file, Company.company_name).join(Company).filter_by(company_id = f'{company_identifier}').all()

        if len(result) is 0:
            return {"errorCode": 404, "Message": "No templates found within company"}, 404

        templates = [
            dict(
                template_id = row['template_id'],
                template_file = row['template_file'],
                )
                for row in result
        ]
        Dict = {}
        Dict["company_name"] = result[0].company_name
        Dict["user_role"] = session["role_role_id"]
        Dict["templates"] = templates
        return Dict, 200

    if request.method == "POST": #Add a template to specific company as KYNDA_ADMIN

        user_verification = verify_user(company_identifier, [1]) #make sure user is logged in correctly
        if user_verification != "PASSED":
            return user_verification

        uploaded_template = request.files['template_file']
        if uploaded_template.filename == '': 
            return {"errorCode": 405, "Message": "No template file found in request, OR File has no valid name"}, 405

        if not (uploaded_template.filename.endswith(".html") or uploaded_template.filename.endswith(".htm")):
            return  {"errorCode": 405, "Message": "No template file found in request, OR File has no valid extension (.html OR .htm)"}, 405

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        uploaded_template.save(random_file_path) #Save template to created storage
        upload_attempt = try_to_upload_file_ftps(random_file_path, f"{uploaded_template.filename}", "templates", company_identifier)

        os.remove(random_file_path)
        if upload_attempt is not "PASSED":
            return upload_attempt

        #New Template object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_template = Template(None, f"{uploaded_template.filename}", company_identifier)

        with create_db_session() as db_session:
            db_session.add(new_template)
            db_session.commit()

        return {"Code": 201, "Message": "Template added to company"}, 201

@template_api.route("/template/<int:company_identifier>/<int:template_identifier>", methods=["GET", "DELETE", "PUT"])
def template(company_identifier, template_identifier):

    if request.method == "GET": #Open specific template (to view or to create a product)
        user_verification = verify_user(company_identifier)
        if user_verification != "PASSED":
            return user_verification

        #result = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
        with create_db_session() as db_session:
            template_file_location_ftp = db_session.query(Template.template_file).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()

        if template_file_location_ftp is not None:
            #print(type(template_file_location_ftp.template_file), template_file_location_ftp.template_file)

            template_bytes = try_to_get_file_ftps_binary(template_file_location_ftp.template_file, "templates", company_identifier)
            if type(template_bytes) is tuple: #Dict means something went wrong, the error code + message defined in try_to_get_text_file will be returned
                return template_bytes

            return send_file(template_bytes, mimetype="text/html")

        return {"errorCode": 404, "Message": "Template Does not exist"""}, 404


    if request.method == "PUT": #Update a specific product as KYNDA_ADMIN
        user_verification = verify_user(company_identifier, [1])
        if user_verification != "PASSED":
            return user_verification

        updated_template = request.files["updated_template"]

        with create_db_session() as db_session:
            old_template_object = db_session.query(Template).filter_by(template_id = template_identifier).first()

        if old_template_object is None:
            return {"errorCode": 404, "Message": "No template with this ID in company found in database"}, 404

        if updated_template.filename != old_template_object.template_file: 
            return {"errorCode": 404, "Message": "No valid file found in request (Name should be same as old product name"}, 404

        #Remove the old file from the templates dir
        attempt_to_remove = try_to_delete_file_ftps(old_template_object.template_file, "template", company_identifier)
        if attempt_to_remove is not "PASSED":
            return attempt_to_remove
        
        #Add the new file to templates dir
        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if os.path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        updated_template.save(random_file_path) #Save template to created storage

        upload_attempt = try_to_upload_file_ftps(random_file_path, f"{updated_template.filename}", "templates", company_identifier)
        os.remove(random_file_path)
        if upload_attempt is not "PASSED":
            return upload_attempt

        return {"Code": 201, "Message": "File succesfully updated"}, 201

    if request.method == "DELETE" : #Delete a specific template as KYNDA_ADMIN
        user_verification = verify_user(company_identifier, [1])
        if user_verification != "PASSED":
            return user_verification
            
    #TODO: FIND A WAY TO ACCESS THE TEMPLATE FILE WITH ONE QUERY FOR DELETION, INSTEAD OF HAVING TO QUERY TWICE (SPEED INCR, OPTIONAL)
        with create_db_session() as db_session:
            template_to_delete = db_session.query(Template).filter_by(template_id = template_identifier).filter_by(Company_company_id = company_identifier).first()
            if template_to_delete is None:
                return {"Code": 404, "Message": "Template not found in database"}, 404

            path = template_to_delete.template_file
            attempt_to_remove = try_to_delete_file_ftps(path, 'templates', company_identifier)
            if attempt_to_remove is not "PASSED":
                return attempt_to_remove

            db_session.delete(template_to_delete)
            db_session.commit()
            
        return attempt_to_remove