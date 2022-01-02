from flask import Blueprint, request, jsonify, send_file
from user_verification import verify_user
from ftp_controller import try_to_get_text_file_ftps, delete_file_ftps, upload_file
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

product_api = Blueprint('product_api', __name__)

@product_api.route("/products/<company_identifier>", methods=["GET", "POST"])
def products(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()

    if request.method == "GET": #View ALL products from a company
        #SELECT `Product_id`, `Product_file`, Company_name WHERE `Company_1` = company_identifier
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
            return {"errorCode": 404, "Message": "No product in company"""}

    if request.method == "POST": #Add a product to DB and FTP
        uploaded_product = request.files['product_file']
        if uploaded_product.filename == '': 
            return {"Code": 405, "Message": "No product file found in request, OR File has no valid name"}

        if not (uploaded_product.filename.endswith(".html") or uploaded_product.filename.endswith(".htm")):
            return  {"Code": 405, "Message": "No product file found in request, OR File has no valid extension (.html OR .htm)"}

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage + create an empty file with given length + extension
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        uploaded_product.save(random_file_path) #Save product to created storage
        upload_file(random_file_path, f"{uploaded_product.filename}", "products", company_identifier)

        os.remove(random_file_path)

        #New Product object is created, None is used for id as it is auto-incremented by SQLAlchemy
        new_product = Product(None, f"{uploaded_product.filename}", company_identifier)
        
        db_session.add(new_product)
        db_session.commit()

        return {"Code": 201, "Message": "Product added to company"}

@product_api.route("/product/<int:company_identifier>/<int:product_identifier>", methods=["GET", "DELETE"])
def product(company_identifier, product_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()

    if request.method == "GET": #Download specific product as client
        #result = db_session.query(Product).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()
        product_file_location_ftp = db_session.query(Product.product_file).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()

        if product_file_location_ftp is not None:
            #print(type(product_file_location_ftp.product_file), product_file_location_ftp.product_file)

            product_bytes = try_to_get_text_file_ftps(product_file_location_ftp.product_file, "products", company_identifier)
            if product_bytes is dict: #Dict means something went wrong, the error code + message defined in try_to_get_text_file will be returned
                return product_bytes

            return send_file(product_bytes, mimetype="text/html")

        return {"errorCode": 404, "Message": "Product Does not exist"""}

    if request.method == "DELETE" : #Delete a specific product

    #TODO: FIND A WAY TO ACCESS THE product FILE WITH ONE QUERY FOR DELETION, INSTEAD OF HAVING TO QUERY TWICE (SPEED INCR, OPTIONAL)
        product_to_delete = db_session.query(Product).filter_by(product_id = product_identifier).filter_by(Company_company_id = company_identifier).first()
        if product_to_delete is None:
            return {"Code": 404, "Message": "Product not found in database"}

        path = product_to_delete.product_file
        attempt_to_remove = delete_file_ftps(path, 'products', company_identifier) #TODO: Change 'products' to actual dynamic var (will not work with image files currently (can get type from file path[etc] and then set accordingly))
        #TODO: CHECK Value of attempt to remove is 201, if not, dont unlink from database (File is not removed from)
        db_session.delete(product_to_delete)
        db_session.commit()
        
        return attempt_to_remove