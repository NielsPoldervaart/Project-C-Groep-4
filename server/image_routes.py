from flask import Blueprint, request, jsonify, send_from_directory, send_file
from flask.scaffold import F
from user_verification import verify_user
from ftp_controller import try_to_get_text_file_ftps, delete_file_ftps, upload_file
from database_connection import *
import os
from os import path
from generate_random_path import generate_random_path

image_api = Blueprint('image_api', __name__)










#TODO: sending images

# @image_api.route("/images/<company_identifier>", methods=["GET","POST"])
# def galleries(company_identifier):

#     user_verification = verify_user(company_identifier)
#     if user_verification != "PASSED":
#         return user_verification

#     db_session = create_db_session()
    
#     if request.method == "GET": #View all galleries available to the company
#         #gets the galleries for the company
#         result = db_session.query(Gallery.gallery_id, Gallery.name).filter_by(Company_company_id = f'{company_identifier}').all() #TODO: add Kynda galleries
#         galleries = [
#             dict(
#                 gallery_id = row['gallery_id'],
#                 gallery_name = row['name']
#             )
#             for row in result
#         ]
#         #gets the collections for the galleries
#         for gallery in galleries:
#             result = db_session.query(Collection.collection_id, Collection.name).filter_by(Gallery_gallery_id = gallery['id']).all()
#             collections = [
#                 dict(
#                     collection_id = row['collection_id'],
#                     name = row['name']
#                 )
#                 for row in result
#             ]
#             #gets the first image of the collection
#             for collection in collections:
#                 result = db_session.query(Image.image_path).filter_by(Collection_collection_id = collection['collection_id']).order_by(Image.image_id.desc()).first()
#                 collection['first_image'] = dict(first_image = result['image_path'])
#             gallery['collections'] = collections

#         if len(galleries) is not 0:
#             return jsonify(galleries)
#         else:
#             return {"errorCode": 404, "Message": "There are no galleries available"""}
    
#     if request.method == "POST": #Add a new gallery
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification
            
#         Gallery_name = request.json["name"]
#         if Gallery_name == '':
#             return {"Code": 405, "Message": "No name found in request"}
#         else:
#             new_Gallery = Gallery(None, Gallery_name, company_identifier)
#             db_session.add(new_Gallery)
#             db_session.commit()
#             return {"Code": 201, "Message": "Gallery added to company"}

# @image_api.route("/images/<company_identifier>/<gallery_identifier>", methods=["GET","POST","DELETE"])
# #route is optional (galleries directly to collection)
# def collections(company_identifier,gallery_identifier):

#     user_verification = verify_user(company_identifier)
#     if user_verification != "PASSED":
#         return user_verification

#     db_session = create_db_session()
    
#     if request.method == "GET": #View all collections inside the gallery
#         result = db_session.query(Collection.collection_id, Collection.name).join(Collection).filter_by(Gallery_gallery_id = f'{gallery_identifier}').all()
#         collections = [
#             dict(
#                 collection_id = row['collection_id'],
#                 name = row['name']
#             )
#             for row in result
#         ]
#         #gets the first image of the collection
#         for collection in collections:
#             result = db_session.query(Image.image_path).filter_by(Collection_collection_id = collection['collection_id']).order_by(Image.image_id.desc()).first()
#             collection['first_image'] = dict(first_image = result['image_path'])
            
#         if len(collections) is not 0:
#             return jsonify(collections)
#         else:
#             return {"errorCode": 404, "Message": "There are no collections in this gallery"""}
    
#     if request.method == "POST": #Add a new collection
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification

#         Collection_name = request.json["name"]
#         if Collection_name == '':
#             return {"Code": 405, "Message": "No name found in request"}
#         else:
#             new_Collection = Collection(None, Collection_name, gallery_identifier)
#             db_session.add(new_Collection)
#             db_session.commit()
#             return {"Code": 201, "Message": "Collection added to gallery"}

#     if request.method == "DELETE": #Remove the gallery
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification

#         if Delete_Gallery(db_session, gallery_identifier) == "Removed":
#             return {"Code": 201, "Message": "Gallery has been removed"}
#         else:
#             return {"errorCode": 404, "Message": "Gallery could not be removed"}

# @image_api.route("/images/<company_identifier>/<gallery_identifier>/<collection_identifier>", methods=["GET","POST","DELETE"])
# def images(company_identifier,gallery_identifier,collection_identifier):
#     user_verification = verify_user(company_identifier)
#     if user_verification != "PASSED":
#         return user_verification

#     db_session = create_db_session()
    
#     if request.method == "GET": #View all images inside the collection
#         result = db_session.query(Image.image_id, Image.image_path).filter_by(Collection_collection_id = f'{collection_identifier}').all()
#         images = [
#             dict(
#                 image_id = row['image_id'],
#                 image_path = row['image_path']
#             )
#             for row in result
#         ]
#         if len(images) is not 0:
#             return jsonify(images)
#         else:
#             return {"errorCode": 404, "Message": "There are no images in this collection"""}
#     if request.method == "POST": #TODO: Add a new image 
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification

#         return
#     if request.method == "DELETE": #Remove the collection
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification

#         if Delete_Collection(db_session, collection_identifier) == "Removed":
#             return {"Code": 201, "Message": "Collection has been removed from the gallery"}
#         else:
#             return {"errorCode": 404, "Message": "Collection could not be removed"}

# @image_api.route("/images/<company_identifier>/<gallery_identifier>/<collection_identifier>/<image_identifier>", methods=["GET","DELETE"])
# def image(company_identifier,gallery_identifier,collection_identifier,image_identifier):

#     user_verification = verify_user(company_identifier)
#     if user_verification != "PASSED":
#         return user_verification

#     db_session = create_db_session()
    
#     if request.method == "GET": #View the image
#         result = db_session.query(Image.image_id, Image.image_path).filter_by(image_id = f'{image_identifier}').first()
#         if result is not None:
#             return jsonify(dict(image_id = row['image_id'], image_path = row['image_path']) for row in result)
#         else:
#             return {"errorCode": 404, "Message": "This image does not exist"""}
#     if request.method == "DELETE": #Remove the image
#         verification = verify_user(company_identifier, [1,2])
#         if verification is not "Passed":
#             return verification

#         if Delete_Image(db_session, collection_identifier, image_identifier) == "Removed":
#             return {"Code": 201, "Message": "Image has been removed from the collection"}
#         else:
#             return {"errorCode": 404, "Message": "Image could not be removed"}




# def Delete_Image(db_session, collection_identifier, image_identifier):
#     image_has_collection_to_delete = db_session.query(Image_has_Collection).filter_by(Image_image_id = image_identifier).filter_by(Collection_collection_id = collection_identifier).all()
#     db_session.delete(image_has_collection_to_delete)
#     db_session.commit()
#     remaining = db_session.query(Image_has_Collection).filter_by(Image_image_id = image_identifier).all()
#     if remaining == None:
#         image = db_session.query(Image).filter_by(image_id = image_identifier).first()
#         db_session.delete(image)
#         db_session.commit()
#     return "Removed"

# def Delete_Collection(db_session, collection_identifier):
#     images_in_collection = db_session.query(Image_has_Collection).filter_by(Collection_collection_id = collection_identifier).all()
#     json_images = jsonify(images_in_collection)
#     for image in json_images:
#         Delete_Image(db_session, collection_identifier, image["Image_image_id"])
#     db_session.delete(db_session.query(Collection).filter_by(collection_id = collection_identifier).first())
#     db_session.commit()
#     return "Removed"

# def Delete_Gallery(db_session, gallery_identifier):
#     collections_in_gallery = db_session.query(Collection).filter_by(Gallery_gallery_id = gallery_identifier).all()
#     json_collections = jsonify(collections_in_gallery)
#     for collection in json_collections:
#         Delete_Collection(db_session, collection["collection_id"])
#     Gallery_has_Companys_to_delete = db_session.query(Gallery_has_Company).filter_by(Gallery_gallery_id = gallery_identifier).all()
#     db_session.delete(Gallery_has_Companys_to_delete)
#     db_session.delete(db_session.query(Gallery).filter_by(gallery_id = gallery_identifier).first())
#     db_session.commit()
#     return "Removed"
