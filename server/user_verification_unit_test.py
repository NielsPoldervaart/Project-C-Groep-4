from server import app
import unittest
#import requests
import json
from database_connection import init_db_structure
from user_verification import verify_user

#Existing User
ExistingAccountName = "admin"
ExistingAccountPassword = "KYNDA"
ExistingAccountCompanyID = 1


class TestRoutes(unittest.TestCase):
###Database creation
    #Database initialization
    def test_db_creation(self):
        init_db_structure()


###Login Existing account
    #POST Login pass
    def test_login_pass(self):
        tester = app.test_client(self)
        response = tester.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def verify_user_test(self):
        test = verify_user(ExistingAccountCompanyID, )
        self.assertEqual(test, "PASSED")

if __name__ == "__main__":
    unittest.main()