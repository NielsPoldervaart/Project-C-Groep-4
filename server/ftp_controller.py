from ftplib import FTP
import os
from os import path
import shutil

def delete_files_from_dir(dir):
    for file_object in os.listdir(dir):
            file_object_path = os.path.join(dir, file_object)
            if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)


def get_file_full(file_name, company_id):
    #Check if theres already files in temp storage from previous requests, if so, delete these files
    if path.exists(f'temporary_ftp_storage/{company_id}'):
        delete_files_from_dir(f'temporary_ftp_storage/{company_id}')

    #Create session with FTP
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    #Change directory on FTP to the company's
    session.cwd(f'{company_id}') #TODO: Catch errors if doesnt exist

    #Check if folders already exists from previous requests, if not, create them
    if not path.exists(f'temporary_ftp_storage/{company_id}/templates'):
        os.makedirs(f'temporary_ftp_storage/{company_id}/templates')
        
    #Create the local (temporary) file
    handle = open(f'temporary_ftp_storage/{company_id}/templates/{file_name}', 'w')
    #print("FILENAME: " + file_name)

    #Retrieve file from FTP server and write it to created temp file
    session.retrlines("RETR " + file_name, handle.write)
    session.quit()

def get_image(file_name, company_id=1):
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")
    handle = open(f'database/templates/{file_name}', 'wb')
    print("FILENAME: " + file_name)
    session.retrbinary("RETR " + file_name, handle.write)
    session.quit()

#upload_file () name of file, file type (gallery OR templates)
def upload_file(file_name, file_type, company_id):
    #Create session with FTP
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    #Open file to send
    file_to_send = open(f"temporary_ftp_storage/{company_id}/{file_type}/{file_name}", 'rb')

    #Check if company dir exists on FTP Server, if not, create it
    if f"{company_id}" not in session.nlst():
        session.mkd(f"{company_id}")

    #Change to the company dir
    session.cwd(f'{company_id}')

    session.storbinary("STOR " + file_name, file_to_send)
    session.quit()
    file_to_send.close()
    os.remove(f"temporary_ftp_storage/{company_id}/{file_type}/{file_name}")

def delete_file(file_name, company_id=1):
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")
    session.delete(file_name)
    session.quit()

def createDir():
    pass

def deleteDir():
    pass


#get_file_full(filename, 1)
#get_image("picture.jpg")
#upload_file("template1.html", "templates")
#a = getFileContents(filename)
#ftp.dir()
#delete_file("picture.jpg")
