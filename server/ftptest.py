from ftplib import FTP

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
    session = FTP('145.24.222.235')
    session.login("Controller", "cC2G'Q_&3qY@=D!@")
    handle = open(f'database/templates/{file_name}', 'w')
    print("FILENAME: " + filename)
    session.retrlines("RETR " + filename, handle.write)

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
