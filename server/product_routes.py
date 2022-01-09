import os
from os import path

from flask import Blueprint, jsonify, request, send_file, session

from database_connection import *
from ftp_controller import (delete_file_ftps, try_to_copy_template_to_product,
                            try_to_get_text_file_ftps, upload_file)
from generate_random_path import generate_random_path
from user_verification import verify_user

product_api = Blueprint('product_api', __name__)

@product_api.route("/products/<int:company_identifier>", methods=["GET", "POST"])
def products(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET": #View ALL products from a company
        with create_db_session() as db_session:
            result = db_session.query(Product.product_id, Product.product_file, Company.company_name).join(Company).filter_by(company_id = f'{company_identifier}').all()

        products = [
            dict(
                product_id = row['product_id'],
              product_file = row['product_file'],
                product_name = row['company_name']
                )
                for row in result
        ]  
        if len(products) is not 0:
            return jsonify(products)
        else:
            return {"errorCode": 404, "Message": "No product in company"}

    if request.method == "POST": #Add a product to DB and FTP
        #CHECK IF TEMPLATE EXISTS WITH THE TEMPLATE_FILE, DOWNLOAD TEMPLATE, UPLOAD TEMPLATE TO SERVER
        requested_template_id = request.form['template_id'] #TODO: CHECK IF THIS SHOULD BE TEMPLATE FILE OR ID
            
        with create_db_session() as db_session:
            requested_template_file_name = db_session.query(Template.template_file).filter_by(template_id = requested_template_id).first()

        if requested_template_file_name.template_file is None:
            return {"errorCode": 404, "Message": "No template with this ID in company found in database"}, 404

        attempt_to_upload_product = try_to_copy_template_to_product(requested_template_file_name.template_file, company_identifier)
        if attempt_to_upload_product != ({"Code": 201, "Message": "Product succesfully created"}, 201):
            return attempt_to_upload_product
        #New Product object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_product = Product(None, f"{requested_template_file_name.template_file}", 0, False, 0, requested_template_id, session["user_id"], company_identifier)
        
        with create_db_session() as db_session:
            db_session.add(new_product)
            db_session.commit()

        return attempt_to_upload_product

@product_api.route("/product/<int:company_identifier>/<int:product_identifier>", methods=["GET", "DELETE", "PUT"])
def product(company_identifier, product_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "GET": #Download specific product as client
        #result = db_session.query(Product).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()
        with create_db_session() as db_session:
            product_file_location_ftp = db_session.query(Product.product_file).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()

        if product_file_location_ftp is not None:
            #print(type(product_file_location_ftp.product_file), product_file_location_ftp.product_file)

            product_bytes = try_to_get_text_file_ftps(product_file_location_ftp.product_file, "products", company_identifier)
            if product_bytes is dict: #Dict means something went wrong, the error code + message defined in try_to_get_text_file will be returned
                return product_bytes

            return send_file(product_bytes, mimetype="text/html")

        return {"errorCode": 404, "Message": "Product Does not exist"""}, 404


    if request.method == "PUT": #Update a specific product
        updated_product = request.files["updated_product"]

        with create_db_session() as db_session:
            old_product_object = db_session.query(Product).filter_by(product_id = product_identifier).first()

        if old_product_object is None:
            return {"errorCode": 404, "Message": "No template with this ID in company found in database"}, 404

        if updated_product.filename != old_product_object.product_file: 
            return {"errorCode": 404, "Message": "No valid file found in request (Name should be same as old product name"}, 404

        #Remove the old file from the products dir
        attempt_to_remove = delete_file_ftps(old_product_object.product_file, "products", company_identifier)
        if attempt_to_remove is not "PASSED":
            return attempt_to_remove
        
        #Add the new file to products dir
        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if os.path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        updated_product.save(random_file_path) #Save template to created storage
        upload_file(random_file_path, f"{updated_product.filename}", "products", company_identifier)
        os.remove(random_file_path)

        return {"Code": 201, "Message": "File succesfully updated"}, 201


    if request.method == "DELETE": #Delete a specific product

    #TODO: FIND A WAY TO ACCESS THE product FILE WITH ONE QUERY FOR DELETION, INSTEAD OF HAVING TO QUERY TWICE (SPEED INCR, OPTIONAL)
        with create_db_session() as db_session:
            product_to_delete = db_session.query(Product).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()
        if product_to_delete is None:
            return {"Code": 404, "Message": "Product not found in database"}, 404

        path = product_to_delete.product_file
        attempt_to_remove = delete_file_ftps(path, 'products', company_identifier) #TODO: Change 'products' to actual dynamic var (will not work with image files currently (can get type from file path[etc] and then set accordingly))
        #TODO: CHECK Value of attempt to remove is 201, if not, dont unlink from database (File is not removed from)
        if attempt_to_remove is not "PASSED":
            return attempt_to_remove

        with create_db_session() as db_session:
            db_session.delete(product_to_delete)
            db_session.commit()
        
        return {"Code": 201, "Message": "File succesfully removed from storage"}, 201

@product_api.route("/product/verify/<int:company_identifier>/<int:product_identifier>", methods=["PUT"])
def verify_product(company_identifier, product_identifier):
    #Check perms (user verification (role 1 or 2))
    #Query product from DB
    #Check if request.form["verified"] == True
    #Change verified column to True
    #TODO: If product is not adequate (request.form["verified"] == False), add options to deny
    #Commit to db
    pass

@product_api.route("/product/download/<int:company_identifier>/<int:product_identifier>", methods=["POST"])
def download_product(company_identifier, product_identifier):
    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    if request.method == "POST":
        with create_db_session() as db_session:
            downloaded_product = db_session.query(Product).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()

            if downloaded_product is None:
                return {"Code": 404, "Message": "Product not found in database"}, 404
            
            if downloaded_product.verified == False:
                return {"Code": 402, "Message": "Product has not been verified"}, 402

            downloaded_product.downloads = downloaded_product.downloads + 1
            db_session.commit()

        return {"Code": 201, "Message": "Product successfully downloaded"}, 201
