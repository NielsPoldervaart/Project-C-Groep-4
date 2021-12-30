from flask import Blueprint, request, jsonify, send_from_directory, send_file
from flask.scaffold import F
from user_verification import verify_user
from ftp_controller import get_image, try_to_get_text_file_ftps, delete_file_ftps, upload_file
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

image_api = Blueprint('image_api', __name__)

#TODO: accepted filetypes
#TODO: errorhandling
#TODO: change image[0:10] to just image

@image_api.route("/gallery/<company_identifier>/<gallery_identifier>", methods=["GET","POST"])
def gallery(company_identifier, gallery_identifier):

    db_session = create_db_session('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB')

    if request.method == "GET": #return all images in the gallery
        user_verification = verify_user(company_identifier)
        if user_verification != "PASSED":
            return user_verification

        result = db_session.query(Image.image_id, Image.image_path).filter_by(Gallery_gallery_id = f'{gallery_identifier}').all()
        if result is not None:
            images = []
            
            for row in result:
                img = get_image(row['image_path'], 'gallery', company_identifier)
                if img is not "":
                    images.append(
                        dict(
                            image_id = row['image_id'],
                            image = img[0:10]
                        )
                    )
                else:
                    return {"errorCode": 404, "Message": "One or multiple images could not be retrieved from the FTP server"}
            
            if len(images) is not 0:
                return jsonify(images)

        return {"errorCode": 404, "Message": "There are no images available"}, 404

    if request.method == "POST": #add an image
        user_verification = verify_user(company_identifier, [1,2])
        if user_verification != "PASSED":
            return user_verification

        uploaded_images = request.files.getlist("file[]")
        for image in uploaded_images:
            print(image.filename)
            if image.filename == '': 
                return {"Code": 405, "Message": "One or multiple images does not have a filename"}, 405

            if not image_endswith(image.filename):
                return  {"Code": 405, "Message": "One or multiple images does not have a correct filetype"}, 405

            random_file_path = generate_random_path(24, 'jpg') #Generate random file path for temp storage + create an empty file with given length + extension
            if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
                random_file_path = generate_random_path(24, 'jpg')

            image.save(random_file_path) #Save image to created storage
            upload_attempt = upload_file(random_file_path, f"{random_file_path}", "gallery", company_identifier)
            os.remove(random_file_path)
            
            if not upload_attempt[1] == 201:
                return upload_attempt

            #New Image object is created, None is used for id as it is auto-incremented by SQLAlchemy
            new_image = Image(None, random_file_path, gallery_identifier)
            
            db_session.add(new_image)
            db_session.commit()

        return {"Code": 201, "Message": "Image added to company"}, 201


def image_endswith(filename):
    accepted_files = [".png",".jpg",".jpeg"]
    for type in accepted_files:
        if filename.endswith(type):
            return True
    return False

@image_api.route("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>", methods=["GET","DELETE"])
def image(company_identifier, gallery_identifier, image_identifier):

    db_session = create_db_session('mysql+mysqldb://kynda:u9N3_HM+ARhDYsRQ@kynda-database.cgmcelrbhqyr.eu-west-2.rds.amazonaws.com/KyndaDB')

    if request.method == "GET": #return the image
        user_verification = verify_user(company_identifier)
        if user_verification != "PASSED":
            return user_verification

        result = db_session.query(Image.image_id, Image.image_path).filter_by(image_id = f'{image_identifier}').first()
        if result is not None:
            img = get_image(result["image_path"], 'gallery', company_identifier)
            if img is not "":
                return jsonify(dict(
                    image_id = result["image_id"],
                    image = img[0:10]
                ))
            return {"errorCode": 404, "Message": "This image could not be retrieved from the FTP server"}, 404
        return {"errorCode": 404, "Message": "This image is not available"}, 404

    if request.method == "DELETE": #delete the image
        user_verification = verify_user(company_identifier,[1,2])
        if user_verification != "PASSED":
            return user_verification

        image = db_session.query(Image).filter_by(image_id = f'{image_identifier}').first()
        if image is not None:
            delete_attempt = delete_file_ftps(image.image_path, 'gallery', company_identifier)
            if delete_attempt[1] is not 404:
                db_session.delete(image)
                db_session.commit()
                return {"Code": 201, "Message": "Image has been removed"}, 201
            return delete_attempt
        return {"errorCode": 404, "Message": "Image could not be found in the database"}, 404