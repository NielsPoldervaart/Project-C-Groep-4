from ftplib import FTP
import os
from os import path
import shutil
import io
from generate_random_path import generate_random_path

"""
def delete_files_from_dir(dir):
    for file_object in os.listdir(dir):
            file_object_path = os.path.join(dir, file_object)
            if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)
"""

def try_to_get_text_file_ftps(file_name, company_id):
    session = FTP('145.24.222.235') #Create session with FTP
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
        return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}

    session.cwd(f'{company_id}') #Change directory on FTP to the company's

    if "templates" not in session.nlst(): #Check if templates dir exists on FTP Server, if not, return
        return {"errorCode": 404, "Message": "Company directory does not contain any templates on FTP server"}

    session.cwd("templates") #Change directory on FTP to the company's
    
    random_file_path = generate_random_path(24, 'html') #Generate random file path for temp storage
    if path.exists(f'temporary_ftp_storage/{random_file_path}'): #Check for extreme edge case, if path is same as a different parallel request path
        random_file_path = generate_random_path(24, 'html')

    with open(f'temporary_ftp_storage/{random_file_path}', 'w') as handle: #Create the local (temporary) file
        if f"{file_name}" not in session.nlst(): #Check if actual file exists on FTP Server in the company id directory, if not, return
            return {"errorCode": 404, "Message": "Requested file not found on FTP server"}
        session.retrlines("RETR " + file_name, handle.write) #Retrieve file from FTP server and write it to created temp file

    return_data = io.BytesIO() #Create variable to store the local file contents

    with open(f'temporary_ftp_storage/{random_file_path}', 'rb') as handle: #Write all contents from temporary file to the variable
        return_data.write(handle.read())

    return_data.seek(0) #return variable position to 0 (after writing it ends up at length-1)

    os.remove(f'temporary_ftp_storage/{random_file_path}') #Remove the temporary_file from local storage    
    session.quit() #Close FTP session

    return return_data #Return the extracted Bytes

def get_image(file_name, company_id=1):
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    handle = open(f'database/templates/{file_name}', 'wb')
    #print("FILENAME: " + file_name)
    session.retrbinary("RETR " + file_name, handle.write)
    session.quit()

#upload_file () name of file, file type (gallery OR templates)
def upload_file(file_path, file_name, file_type, company_id):

    session = FTP('145.24.222.235') #Create session with FTP
    session.login("Controller", "cC2G'Q_&3qY@=D!@") #Login to FTP

    file_to_send = open(file_path, 'rb') #Open file to send

    if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, create it
        session.mkd(f"{company_id}")
    session.cwd(f'{company_id}') #Change to the company dir
    if file_type not in session.nlst():
        session.mkd(file_type)

    session.cwd(file_type) #Change to the company dir
    session.storbinary("STOR " + file_name, file_to_send) #Send file as through binary
    session.quit() #Close FTP session
    file_to_send.close()

def delete_file_ftps(file_path, file_type, company_id):
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    if f"{company_id}" not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
        return {"errorCode": 404, "Message": "Company directory does not exist on FTP server"}

    session.cwd(f'{company_id}') #Change to the company dir

    if file_type not in session.nlst(): #Check if company dir exists on FTP Server, if not, return
        return {"errorCode": 404, "Message": "Correct file directory does not exist on FTP server"}

    session.cwd(file_type) #Change to the company dir

    session.delete(file_path)
    session.quit()
    return {"errorCode": 201, "Message": "File succesfully removed from storage"}


#try_to_download_text_file(filename, 1)
#get_image("picture.jpg")
#upload_file("template1.html", "templates")
#a = getFileContents(filename)
#ftp.dir()
#delete_file("picture.jpg")
