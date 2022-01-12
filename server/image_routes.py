from flask import Blueprint, request, jsonify
from user_verification import verify_user
from ftp_controller import try_to_get_image_ftps, try_to_delete_file_ftps, try_to_upload_file_ftps
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

image_api = Blueprint('image_api', __name__)

#TODO: accepted filetypes

@image_api.route("/gallery/<company_identifier>/<gallery_identifier>", methods=["GET","POST"])
def gallery(company_identifier, gallery_identifier):

    if request.method == "GET": #return all images in the gallery
        user_verification = verify_user(company_identifier)
        if user_verification != "PASSED":
            return user_verification

        with create_db_session() as db_session:
            result = db_session.query(Image.image_id, Image.image_path).filter_by(Gallery_gallery_id = f'{gallery_identifier}').all()

        if len(result) == 0:
            return {"errorCode": 404, "Message": "No images found in database with this gallery id"}, 404

        images = []
        for row in result:
            img = try_to_get_image_ftps(row['image_path'], 'gallery', company_identifier)
            if type(img) is tuple: #Tuple means something went wrong 
                return img
            images.append(
                dict(
                    image_id = row['image_id'],
                    image = img
                )
            )
        
        if len(images) is not 0:
            return jsonify(images)
        return {"errorCode": 404, "Message": "There are no images available"}, 404

    if request.method == "POST": #add an image
        user_verification = verify_user(company_identifier, [1,2])
        if user_verification != "PASSED":
            return user_verification

        with create_db_session() as db_session:
            existing_image_names = db_session.query(Image.image_path).filter_by(Gallery_gallery_id = f'{gallery_identifier}').all()

        uploaded_images = request.files.getlist("file[]")
        if uploaded_images == []:
            return {"errorCode": 405, "Message": "No images were sent through the request"}, 405

        for image in uploaded_images:
            if image.filename == '': 
                return {"errorCode": 405, "Message": "One or multiple images does not have a filename"}, 405

            if not image_endswith(image.filename):
                return  {"errorCode": 405, "Message": "One or multiple images does not have a correct filetype"}, 405
            
            if image.filename in existing_image_names:
                return {"errorCode": 402, "Message": "The filename of one or multiple images already exists in the gallery"}, 402

            random_file_path = generate_random_path(24, 'jpg') #Generate random file path for temp storage + create an empty file with given length + extension
            if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
                random_file_path = generate_random_path(24, 'jpg')
            image.save(random_file_path) #Save image to created storage

            upload_attempt = try_to_upload_file_ftps(random_file_path, f"{image.filename}", "gallery", company_identifier)
            os.remove(random_file_path)
            if upload_attempt is not "PASSED":
                return upload_attempt

            #New Image object is created, None is used for id as it is auto-incremented by SQLAlchemy
            new_image = Image(None, image.filename, gallery_identifier)
            with create_db_session() as db_session:
                db_session.add(new_image)
                db_session.commit()

        return {"Code": 201, "Message": "Image(s) added to company"}, 201


def image_endswith(filename): #Check for accepted filenames
    accepted_files = [".png",".jpg",".jpeg"]
    for type in accepted_files:
        if filename.endswith(type):
            return True
    return False

@image_api.route("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>", methods=["GET","DELETE"])
def image(company_identifier, gallery_identifier, image_identifier):

    if request.method == "GET": #return the image
        user_verification = verify_user(company_identifier)
        if user_verification != "PASSED":
            return user_verification

        with create_db_session() as db_session:
            result = db_session.query(Image.image_id, Image.image_path).filter_by(image_id = f'{image_identifier}').filter_by(Gallery_gallery_id = f'{gallery_identifier}').first()
        if result is None:
            return {"errorCode": 404, "Message": "This image is not available"}, 404

        img = try_to_get_image_ftps(result["image_path"], 'gallery', company_identifier)
        if type(img) is tuple: #TUPLE MEANS SOMETHING WENT WRONG
            return img

        return dict(
            image_id = result["image_id"],
            image = img
        ), 200

    if request.method == "DELETE": #delete the image
        user_verification = verify_user(company_identifier,[1,2])
        if user_verification != "PASSED":
            return user_verification

        with create_db_session() as db_session:
            image = db_session.query(Image).filter_by(image_id = f'{image_identifier}').first()
            if image is None:
                return {"errorCode": 404, "Message": "Image could not be found in the database"}, 404

            delete_attempt = try_to_delete_file_ftps(image.image_path, 'gallery', company_identifier)
            if delete_attempt is not "PASSED":
                return delete_attempt
    
            db_session.delete(image)
            db_session.commit()
            return {"Code": 201, "Message": "Image has been removed"}, 201

