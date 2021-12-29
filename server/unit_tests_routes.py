from server import app
import unittest
#import requests
import json
from database_connection import init_db_structure
from user_verification import verify_user

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

tester = None

class TestRoutes(unittest.TestCase):
###Database creation
    #Database initialization
    def setUp(self):
        init_db_structure()


###TODO: Security tests before logging in
    #TODO: TEST Company routes
    #TODO: TEST Template routes
    #TODO: TEST Product routes
    #TODO: TEST image routes

###Login Existing account
    #POST Login fail ALL
    """
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
    """

    
    def test_all(self):
        client = app.test_client(self)
        self.login_pass(client)
        self.template_pass(client)
        

    def login_pass(self, client):
        response = client.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response


    def template_pass(self, client):
        response = client.get(f"/templates/{ExistingAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    #POST Login pass
    """
    def test_login_pass(self):
        with app.test_client() as client:
            response = client.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
    """    

###TODO: Register new accounts
    #TODO: Register throwaway account (verification should get declined)
    #TODO: Register actual account (verification should get accepted)

###TODO: Company routes (View all accounts)
    #TODO: GET view company info pass ("/company/<company_identifier>" GET)
    #TODO: GET view company accounts info pass ("/<company_identifier>/accounts" GET)
    #TODO: GET view company manual ("/<company_identifier>/manual" GET)
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
    """
    def test_template_pass(self):
        with app.test_client() as client:
            response = client.get(f"/templates/{ExistingAccountCompanyID}")
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
    """
        
    #TODO: GET view specific template ("/template/<int:company_identifier>/<int:template_identifier>" GET)
    #TODO: DELETE specific template ("/template/<int:company_identifier>/<int:template_identifier>" DELETE)

###TODO: Product routes
    #TODO: 


###TODO: Images routes
    #TODO: 

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