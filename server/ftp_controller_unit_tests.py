from server import app
from werkzeug.security import generate_password_hash
import unittest
from database_connection import *
from user_verification import verify_user
import os

#Existing User
ExistingAccountName = "admin"
ExistingAccountPassword = "KYNDA"
ExistingAccountCompanyID = 1

class Test_user_verification_module(unittest.TestCase):
###Database creation
    #Database initialization
    
    def setUp(self):
        #init_db_structure("sqlite://")
        #setup_basic_db()
        pass
    
    def test_ftp_controller(self):
        with app.test_client() as client:
            with app.app_context():
                self.create_db_and_insert_values()
            client.get("/") #Create a session by requesting index route
            self.verify_user_fail()
            self.login_pass(client)
            self.verify_user_pass()
            self.verify_user_fail_access()
            self.verify_user_fail_company()
            self.verify_user_fail_company_access()

    def create_db_and_insert_values(self): #CREATES DATABASE FILE + STRUCTURE AND INSERTS NECESSARY VALUES
        init_db_structure()
        with create_db_session() as db_session:
            db_session.add(Role(None, "KYNDA_ADMIN"))
            db_session.add(Role(None, "COMPANY_ADMIN"))
            db_session.add(Role(None, "COMPANY_EMPLOYEE"))
            db_session.add(Gallery(None, "Kynda_gallery"))
            db_session.add(Company(None, "Kynda", 1, None))
            db_session.add(User(None, "admin", generate_password_hash("admin@hr.nl"), generate_password_hash("KYNDA"), True, 1, 1))
            db_session.commit()

###Login Existing account (KYNDA_ADMIN (ROLE=1))
    #POST Login pass
    def verify_user_fail(self):
        test = verify_user(ExistingAccountCompanyID) 
        self.assertEqual(test, ({"errorCode" : 401, "Message" : "Login not authorized"}, 401))

    def login_pass(self, client):
        response = client.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

    #CHECK IF MODULE WORKS WITH ALL ROLES ENABLED AND CORRECT COMPANY_ID
    def verify_user_pass(self):
        test = verify_user(ExistingAccountCompanyID) 
        self.assertEqual(test, "PASSED")

    #CHECK IF MODULE WORKS WITH ROLES ENABLED THAT ARE NOT IN USER HIS ROLE, BUT WITH CORRECT COMPANY_ID
    def verify_user_fail_access(self):
        test = verify_user(ExistingAccountCompanyID, [2,3]) 
        self.assertEqual(test, ({"errorCode" : 403, "Message" : "Required Role not within User's roles"}, 403))

    #CHECK IF MODULE WORKS WHEN LOGGED INTO THE WRONG COMPANY, BUT WITH ALL ROLES ENABLED
    def verify_user_fail_company(self):
        test = verify_user(-1) 
        self.assertEqual(test, ({"errorCode" : 403, "Message" : "Company not within User's companies"}, 403))

    #CHECK IF MODULE WORKS WHEN LOGGED INTO THE WRONG COMPANY AND WITH ROLES ENABLED THAT ARE NOT IN USER HIS ROLE
    def verify_user_fail_company_access(self):
        test = verify_user(-1, [4,5]) 
        self.assertEqual(test, ({"errorCode" : 403, "Message" : "Company not within User's companies"}, 403))

    #CREATE TEST FOLDER
    #TRY TO RETRIEVE TEMPLATE WHEN THERES NOTHING IN FTP
    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    #SEND TEMPLATE TO SERVER
    #MAKE PRODUCT
    #SEND IMAGE TO SERVER
    #REMOVE TEMPLATE
    #REMOVE PRODUCT
    #REMOVE IMAGE
    #DELETE TEST FOLDER


    def tearDown(self):
        os.remove("test_sqlite.db")

if __name__ == "__main__":
    unittest.main()