from ftplib import FTP
import os
from os import path
import shutil
import io
import random
import string

def delete_files_from_dir(dir):
    for file_object in os.listdir(dir):
            file_object_path = os.path.join(dir, file_object)
            if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

def get_file_full(file_name, company_id):

    #Create session with FTP
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    #Change directory on FTP to the company's
    session.cwd(f'{company_id}') #TODO: Catch errors if doesnt exist

    #Generate random file path for temp storage
    random_file_path = f'{get_random_string(24)}.html'

    #Check for extreme edge case, if path is same as a different parallel request path
    if path.exists(f'temporary_ftp_storage/{random_file_path}'):
        random_file_path = f'{get_random_string(24)}.html'
        
    #Create the local (temporary) file
    with open(f'temporary_ftp_storage/{random_file_path}', 'w') as handle:
        #Retrieve file from FTP server and write it to created temp file
        session.retrlines("RETR " + file_name, handle.write)

    #Create variable to store the local file contents
    return_data = io.BytesIO()
    with open(f'temporary_ftp_storage/{random_file_path}', 'rb') as handle:
        #Write all contents from temporary file to the variable
        return_data.write(handle.read())
    #return variable position to 0 (after writing it ends up at length-1)
    return_data.seek(0)

    #Remove the temporary_file from local storage
    os.remove(f'temporary_ftp_storage/{random_file_path}')
    
    #Close FTP session
    session.quit()

    #Return the extracted Bytes
    return return_data

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

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



#get_file_full(filename, 1)
#get_image("picture.jpg")
#upload_file("template1.html", "templates")
#a = getFileContents(filename)
#ftp.dir()
#delete_file("picture.jpg")
