from flask import Blueprint, request, jsonify, send_from_directory, send_file
from user_verification import verify_user
from ftp_controller import try_to_get_text_file_ftps, delete_file_ftps, upload_file
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

image_api = Blueprint('image_api', __name__)

@image_api.route("/images/<company_identifier>", methods=["GET","POST"])
def galleries(company_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()
    
    if request.method == "GET": #View all galleries available to the company
        result = db_session.query(Gallery.gallery_id, Gallery.name, Company.company_id).join(Gallery_has_Company).filter_by(gallery_id = Gallery_has_Company.Gallery_gallery_id).join(Company).filter_by(Company_company_id = f'{company_identifier}').all()
        galleries = [
            dict(
                gallery_id = row['gallery_id'],
                gallery_name = row['name'],
                company_id = row['company_id']
            )
            for row in result
        ]
        if len(galleries) is not 0:
            return jsonify(galleries)
        else:
            return {"errorCode": 404, "Message": "There are no galleries available"""}
    if request.method == "POST": #Add a new gallery (when user is Kynda employee)
        return

@image_api.route("/images/<company_identifier>/<gallery_identifier>", methods=["GET","POST","DELETE"])
def collections(company_identifier,gallery_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()
    
    if request.method == "GET": #View all collections inside the gallery
        result = db_session.query(Collection.collection_id, Collection.name).join(Collection).filter_by(Gallery_gallery_id = f'{gallery_identifier}').all()
        collections = [
            dict(
                collection_id = row['collection_id'],
                name = row['name']
            )
            for row in result
        ]
        if len(collections) is not 0:
            return jsonify(collections)
        else:
            return {"errorCode": 404, "Message": "There are no collections in this gallery"""}
    if request.method == "POST": #Add a new collection (when user is Kynda employee)
        Collection_name = request.json["name"]
        if Collection_name == '':
            return {"Code": 405, "Message": "No name found in request"}

        else:
            new_Collection = Collection(None, Collection_name, gallery_identifier)
            db_session.add(new_Collection)
            db_session.commit()
            return {"Code": 201, "Message": "Collection added to gallery"}
    if request.method == "DELETE": #Remove the gallery (when user is Kynda employee)
        return

@image_api.route("/images/<company_identifier>/<gallery_identifier>/<collection_identifier>", methods=["GET","POST","DELETE"])
def images(company_identifier,gallery_identifier,collection_identifier):
    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()
    
    if request.method == "GET": #View all images inside the collection
        result = db_session.query(Image.image_id, Image.image_path).join(Image_has_Collection).filter_by(Collection_collection_id = f'{collection_identifier}').filter_by(Image_id = Image_has_Collection.Image_image_id).all()
        images = [
            dict(
                image_id = row['image_id'],
                image_path = row['image_path']
            )
            for row in result
        ]
        if len(images) is not 0:
            return jsonify(images)
        else:
            return {"errorCode": 404, "Message": "There are no images in this collection"""}
    if request.method == "POST": #Add a new image (when user is Kynda employee)
        return
    if request.method == "DELETE": #Remove the collection (when user is Kynda employee)
        return

@image_api.route("/images/<company_identifier>/<gallery_identifier>/<collection_identifier>/<image_identifier>", methods=["GET","DELETE"])
def image(company_identifier,gallery_identifier,collection_identifier,image_identifier):

    user_verification = verify_user(company_identifier)
    if user_verification != "PASSED":
        return user_verification

    db_session = create_db_session()
    
    if request.method == "GET": #View the image
        result = db_session.query(Image.image_id, Image.image_path).filter_by(image_id = f'{image_identifier}').first()
        if result is not None:
            return jsonify(dict(image_id = row['image_id'], image_path = row['image_path']) for row in result)
        else:
            return {"errorCode": 404, "Message": "This image does not exist"""}
    if request.method == "DELETE": #Remove the image (when user is Kynda employee)
        return