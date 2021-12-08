from ftplib import FTP
import os
import shutil

contents = []
filename = 'test.html'

def getFileContents(filename, company_id=0):
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")

    global contents
    session.retrlines("RETR " + filename, collectLines)
    tempContents = contents
    contents = []
    return tempContents

def get_file_full(file_name, company_id):
    folder_path = 'database\\templates'
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")
    handle = open(f'database/templates/{file_name}', 'w')
    print("FILENAME: " + file_name)
    session.retrlines("RETR " + file_name, handle.write)

def uploadFile():
    pass

def updateFile():
    pass

def deleteFile():
    pass
def createDir():
    pass

def deleteDir():
    pass

def collectLines(s):
    global contents
    contents.append(s)

#get_file_full(filename, 1)
#a = getFileContents(filename)
#ftp.dir()
