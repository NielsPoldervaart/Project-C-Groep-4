from server import app
import unittest
from database_connection import *
from user_verification import verify_user

#Existing User
ExistingAccountName = "admin"
ExistingAccountPassword = "KYNDA"
ExistingAccountCompanyID = 1

class Test_user_verification_module(unittest.TestCase):
###Database creation
    #Database initialization
    """
    def setUp(self):
        init_db_structure("sqlite://")
    """
    def test_user_verification(self):
        with app.test_client() as client:
            client.get("/") #Create a session by requesting index route 
            client.get("/init")
            self.verify_user_fail()
            self.login_pass(client)
            self.verify_user_pass()
            self.verify_user_fail_access()
            self.verify_user_fail_company()
            self.verify_user_fail_company_access()

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

if __name__ == "__main__":
    unittest.main()