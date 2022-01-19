from ftplib import FTP
import os
from os import path
import io
from generate_random_path import generate_random_path
from flask import current_app

import base64

accepted_extensions_template = [".htm", ".html"]
accepted_extensions_image = [".jpg", ".jpeg", ".png"]


def try_to_get_file_ftps_binary(file_name, file_type, company_id):
    #session = FTP('145.24.222.235') #Create session with FTP
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@")

        if current_app.config["USING_TEST_FTP"]: #If testing == True, we dont want to use regular storage, change to specific ftp storage
            if "testfolder" not in session.nlst():
                return {"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404
            session.cwd("testfolder")

        if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}, 404

        session.cwd(f'{company_id}') #Change directory on FTP to the company's

        if file_type not in session.nlst(): #Check if file_type dir exists on FTP Server, if not, return (EG: "templates", "manual")
            return {"errorCode": 404, "Message": f"Company directory does not contain any {file_type} on FTP server"}, 404

        session.cwd(file_type) #Change directory on FTP to the company's
        
        if f"{file_name}" not in session.nlst(): #Check if actual file exists on FTP Server in the company id directory, if not, return
            return {"errorCode": 404, "Message": "Requested file not found on FTP server"}, 404

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        with open(f'temporary_ftp_storage/{random_file_path}', 'wb') as handle: #Create the local (temporary) file
            session.retrbinary("RETR " + file_name, handle.write) #Retrieve file from FTP server and write it to created temp file

        return_data = io.BytesIO() #Create variable to store the local file contents

        with open(f'temporary_ftp_storage/{random_file_path}', 'rb') as handle: #Write all contents from temporary file to the variable
            return_data.write(handle.read())

        return_data.seek(0) #return variable position to 0 (after writing it ends up at length-1)

        os.remove(f'temporary_ftp_storage/{random_file_path}') #Remove the temporary_file from local storage    

        return return_data #Return the extracted Bytes

def try_to_get_image_ftps(file_name, file_type, company_id):
    #session = FTP('145.24.222.235')
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@")

        if current_app.config["USING_TEST_FTP"]: #If testing == True, we dont want to use regular storage, change to specific ftp storage
            if "testfolder" not in session.nlst():
                return {"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404
            session.cwd("testfolder")
        
        if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}, 404

        session.cwd(f'{company_id}') #Change directory on FTP to the company's

        if file_type not in session.nlst(): #Check if file_type dir exists on FTP Server, if not, return (EG: "templates", "manual")
            return {"errorCode": 404, "Message": f"Company directory does not contain any {file_type} on FTP server"}, 404

        session.cwd(file_type) #Change directory on FTP to the company's
        
        random_file_path = generate_random_path(24, 'jpg') #Generate random file path for temp storage
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'jpg')

        with open(f'temporary_ftp_storage/{random_file_path}', 'wb') as handle:
            session.retrbinary("RETR " + file_name, handle.write)
        img = ""
        with open(f'temporary_ftp_storage/{random_file_path}', 'rb') as f:
            for data in f:
                img_b64 = base64.b64encode(data)
                img_str = img_b64.decode('ascii')
                img = img + img_str
        os.remove(f'temporary_ftp_storage/{random_file_path}')
        return img

#Copies a company's template into a company's product directory on FTP
def try_to_copy_template_to_product(template_name, company_id):
    #session = FTP('145.24.222.235') #Create session with FTP
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@")

        if current_app.config["USING_TEST_FTP"]: #If testing == True, we dont want to use regular storage, change to specific ftp storage
            if "testfolder" not in session.nlst():
                return {"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404
            session.cwd("testfolder")

        if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}, 404

        session.cwd(f'{company_id}') #Change directory on FTP to the company's

        if "templates" not in session.nlst(): #Check if templates dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": f"Company directory does not contain any on FTP server"}, 404

        session.cwd("templates") #Change directory on FTP to the company's
        
        if f"{template_name}" not in session.nlst(): #Check if actual file exists on FTP Server in the company id directory, if not, return
            return {"errorCode": 404, "Message": "Requested file not found on FTP server"}, 404

        random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage
        if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
            random_file_path = generate_random_path(24, 'html')

        with open(f'temporary_ftp_storage/{random_file_path}', 'wb') as handle: #Create the local (temporary) file
            session.retrbinary("RETR " + template_name, handle.write) #Retrieve file from FTP server and write it to created temp file

        session.cwd("../") #Back out of templates dir 

        if "products" not in session.nlst(): #Check if products dir exists on FTP Server, if not, create it
            session.mkd("products")
        session.cwd("products")
        with open(f'temporary_ftp_storage/{random_file_path}', 'rb') as file_to_send:
            session.storbinary("STOR " + template_name , file_to_send)

        os.remove(f"temporary_ftp_storage/{random_file_path}")
        return {"Code": 201, "Message": "Product succesfully created"}, 201


#try_to_upload_file_ftps () name of file, file type (gallery OR templates)
def try_to_upload_file_ftps(file_path, file_name, file_type, company_id):

    #session = FTP('145.24.222.235') #Create session with FTP
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@") #Login to FTP

        if current_app.config["USING_TEST_FTP"]: #If testing == True, we dont want to use regular storage, change to specific ftp storage
            if "testfolder" not in session.nlst():
                session.mkd("testfolder")
            session.cwd("testfolder")

        if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, create it
            session.mkd(f"{company_id}")
        session.cwd(f'{company_id}') #Change to the company dir
        if file_type not in session.nlst(): #file_type = template, product or gallery
            session.mkd(file_type)

        if not(os.path.isfile(file_path)):
            return {"errorCode": 404, "Message": "No file found in request"}, 404
        file_extension = os.path.splitext(file_path)[-1].lower()


        if file_extension in accepted_extensions_template: #TODO: NICE_TO_HAVE: CHANGE THIS INTO SEPARATE FUNCTIONS
            if file_type == "manual":
                session.cwd("manual")
            elif file_type == "templates":    
                session.cwd("templates") #Change to the gallery/templates dir
            elif file_type == "products":
                session.cwd("products")
            else:
                return {"errorCode": 404, "Message": "Extension not supported for this type of file"}, 404

        elif file_extension in accepted_extensions_image:
            if file_type == "gallery":
                session.cwd("gallery")
            else: 
                return {"errorCode": 404, "Message": "Extension not supported for this type of file"}, 404
        else:
            {"errorCode": 404, "Message": "No valid extension"}, 404

        with open(file_path, 'rb') as file_to_send: #Open file to send
            session.storbinary("STOR " + file_name, file_to_send) #Send file through as binary
        return "PASSED"

def try_to_delete_file_ftps(file_path, file_type, company_id):
    #session = FTP('145.24.222.235')
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@")
        if current_app.config["USING_TEST_FTP"]: #If testing == True, we dont want to use regular storage, change to specific ftp storage
            if "testfolder" not in session.nlst():
                return {"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404
            session.cwd("testfolder")

        if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}, 404

        session.cwd(f'{company_id}') #Change to the company dir

        if file_type not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": "Correct file directory does not exist on FTP server"}, 404

        session.cwd(file_type) #Change to the file_type dir (EG: products, templates)

        if file_path not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
            return {"errorCode": 404, "Message": f"File does not exist on FTP server"}, 404

        session.delete(file_path)
        return "PASSED"

def delete_test_folder_ftp():
    with FTP('145.24.222.235') as session:
        session.login("Controller", "cC2G'Q_&3qY@=D!@")
        if "testfolder" not in session.nlst():
            return 1

        deletedir("testfolder", session)
        return 0

def deletedir(dirname, ftp):
    ftp.cwd(dirname)
    for file in ftp.nlst():
        try:
            ftp.delete(file)
        except Exception:
            deletedir(file, ftp)
    ftp.cwd("..")
    ftp.rmd(dirname)

#try_to_download_text_file(filename, 1)
#try_to_get_image_ftps("picture.jpg")
#try_to_upload_file_ftps("template1.html", "templates")
#a = getFileContents(filename)
#ftp.dir()
#delete_file("picture.jpg")
