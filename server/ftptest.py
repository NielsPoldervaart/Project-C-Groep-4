from ftplib import FTP

session = FTP('145.24.222.235')
session.login("Controller", "cC2G'Q_&3qY@=D!@")

contents = []
filename = 'test.html'

def getFile(filename, company_id=0):
    global contents
    session.retrlines("RETR " + filename, collectLines)
    tempContents = contents
    contents = []
    return tempContents

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

getFile(filename)
print(contents)
#ftp.dir()
