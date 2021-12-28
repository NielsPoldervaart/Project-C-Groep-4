from server import app
import unittest
#import requests
import json
from database_connection import init_db_structure


###Global variables
#Fake User
FakeAccountName = ""
FakeAccountPassword = ""

#Existing User
ExistingAccountName = "admin"
ExistingAccountPassword = "KYNDA"
ExistingAccountCompanyID = 1

#Throwaway account
ThrowawayAccountName = "" #TODO: Create random values (random path function, daytime function, etc...)
ThrowawayAccountPassword = ""
ThrowawayAccountCompanyID = -1
#Created account
CreatedAccountName = ""
CreatedAccountPassword = ""
CreatedAccountCompanyID = -1

class TestRoutes(unittest.TestCase):
###Database creation
    #Database initialization
    def test_db_creation(self):
        init_db_structure()

###TODO: Security tests before logging in
    #TODO: TEST Company routes
    #TODO: TEST Template routes
    #TODO: TEST Product routes
    #TODO: TEST image routes

###Login Existing account
    #POST Login fail ALL
    def test_login_fail_all(self):
        tester = app.test_client(self)
        response = tester.post("/login", json={"name":FakeAccountName, "password":FakeAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)

    #POST Login fail PASSWORD
    def test_login_fail_password(self):
        tester = app.test_client(self)
        response = tester.post("/login", json={"name":ExistingAccountName, "password":FakeAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)

    #POST Login fail USERNAME
    def test_login_fail_username(self):
        tester = app.test_client(self)
        response = tester.post("/login", json={"name":FakeAccountName, "password":ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)

    #POST Login pass
    def test_login_pass(self):
        tester = app.test_client(self)
        response = tester.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


###TODO: Register new accounts
    #TODO: Register throwaway account (verification should get declined)
    #TODO: Register actual account (verification should get accepted)

###TODO: Company routes (View all accounts)
    #TODO: GET view company info pass ("/company/<company_identifier>" GET)
    #TODO: GET view company accounts info pass ("/<company_identifier>/accounts" GET)
    #TODO: POST decline throwaway account ("/<company_identifier>/accounts" POST)
    #TODO: POST verify newly made account ("/<company_identifier>/accounts" POST)

###TODO: Logout Existing account
    #TODO: Logout pass

###TODO: Login Created account
    #TODO: Login pass

###TODO: Template routes
    #TODO: POST add template to company for product creation ("/templates/<company_identifier>" POST)
        #TODO: Create a folder for template to add
    #TODO: POST add template to company for deletion test ("/templates/<company_identifier>" POST)

    #GET view all templates from company ("/templates/<company_identifier>" GET)
    def template_test(self):
        tester = app.test_client(self)
        response = tester.get(f"/templates/{ExistingAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        
    #TODO: GET view specific template ("/template/<int:company_identifier>/<int:template_identifier>" GET)
    #TODO: DELETE specific template ("/template/<int:company_identifier>/<int:template_identifier>" DELETE)

###TODO: Product routes
    #TODO: 


###TODO: Image routes
    #TODO: GET view all images of gallery ("/gallery/<company_identifier>/<gallery_identifier>" GET)
    #TODO: POST try to add a file with the wrong filetype ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    #TODO: POST add an image for *later use* ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    #TODO: POST add an image to delete ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    #TODO: GET view the selected images from gallery ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" GET)
    #TODO: DELETE remove the image to be deleted ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" DELETE)

###TODO: Guide routes
    #TODO: 

###TODO: Logout Created account
    #TODO: Logout pass

###TODO: Security tests after logging out
    #TODO: TEST Company routes
    #TODO: TEST Template routes
    #TODO: TEST Product routes
    #TODO: TEST image routes

if __name__ == "__main__":
    unittest.main()