from server import app
import unittest
#import requests
import json
from db_controller import setup_basic_db
from user_verification import verify_user
from database_connection import *
from werkzeug.security import generate_password_hash
import os

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
        pass

    def test_routes(self):
        with app.test_client() as client:
            with app.app_context():
                setup_basic_db()
            client.get("/") #Create a session by requesting index route
 
            #SECURITY TESTS BEFORE LOGGING IN #SEBASTIAAN BOOMAN
            #self.company_route_security_test(client)
            #self.template_route_security_test(client)
            #self.product_route_security_test(client)
            #self.image_route_security_test(client)

            #LOGIN EXISTING ACCOUNT
            self.login_fail_all(client)
            self.login_fail_password(client)
            self.login_fail_username(client)
            self.login_pass(client)

            #REGISTER NEW ACCOUNTS
            #self.register_throwaway_account_pass(client) #
            #self.register_actual_account_pass(client) #

            #COMPANY ROUTES
            #self.company_info_pass(client) #
            #self.company_accept_account_pass(client) #
            #self.company_add_manual_pass(client) #
            #self.company_view_manual_pass(client) #
            #self.company_accept_account_pass(client) #
            #self.company_decline_account_pass(client) #

            #LOGOUT EXISTING ACCOUNT
            #self.logout_existing_account_pass(client)

            #LOGIN CREATED ACCOUNT
            #self.login_created_account_pass(self)

            #TEMPLATE ROUTES TOM SCHREUR
            self.view_all_templates_empty_pass(client)
            #self.upload_template_filetype_fail(client)
            #self.upload_template_for_creation_pass(client)
            #self.upload_template_for_deletion_pass(client)
            self.view_all_templates_exists_pass(client)
            #self.view_specific_template_exists_pass(client)
            #self.delete_specific_template_exists_pass(client)

            #PRODUCT ROUTES
            #self.create_product_pass(client)
            #self.alter_product_pass(client)
            #self.delete_product_pass(client)

            #IMAGE ROUTES
            #self.view_all_images_empty_pass(client)
            #self.upload_image_filetype_fail(client)
            #self.upload_image_pass(client)
            #self.view_specific_image_pass(client)
            #self.remove_specific_image_pass(client)

            #LOGOUT CREATED ACCOUNT
            #self.logout_created_account_pass(client)

            #SECURITY TESTS AFTER LOGGING OUT
            #self.company_route_security_test2(client)
            #self.template_route_security_test2(client)
            #self.product_route_security_test2(client)
            #self.image_route_security_test2(client)

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

###TODO: Security tests before logging in
    #TODO: TEST Company routes
    def company_route_security_test(self, client):
        pass

    #TODO: TEST Template routes
    def template_route_security_test(self, client):
        pass

    #TODO: TEST Product routes
    def product_route_security_test(self, client):
        pass

    #TODO: TEST image routes
    def image_route_security_test(self, client):
        pass

###Login Existing account

    #POST Login fail ALL
    def login_fail_all(self, client):
        response = client.post("/login", json={"name":FakeAccountName, "password":FakeAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)
        return response

    #POST Login fail PASSWORD
    def login_fail_password(self, client):
        response = client.post("/login", json={"name":ExistingAccountName, "password":FakeAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)
        return response

    #POST Login fail USERNAME
    def login_fail_username(self, client):
        response = client.post("/login", json={"name":FakeAccountName, "password":ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 406)
        return response

    #POST Login pass
    def login_pass(self, client):
        response = client.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

###TODO: Register new accounts
    #TODO: Register throwaway account (verification should get declined)
    def register_throwaway_account_pass(self, client):
        pass
    #TODO: Register actual account (verification should get accepted)
    def register_actual_account_pass(self, client):
        pass

###TODO: Company routes (View all accounts)
    #TODO: GET view company info pass ("/company/<company_identifier>" GET)
    def company_info_pass(self, client):
        pass
    #TODO: GET view company accounts info pass ("/<company_identifier>/accounts" GET)
    def company_accounts_info_pass(self, client):
        pass
    #TODO: POST Insert a company manual ("/<company_identifier>/manual" POST)
    def company_add_manual_pass(self, client):
        pass
    #TODO: GET view company manual ("/<company_identifier>/manual" GET)
    def company_view_manual_pass(self, client):
        pass
    #TODO: POST decline throwaway account ("/<company_identifier>/accounts" POST)
    def company_accept_account_pass(self, client):
        pass
    #TODO: POST verify newly made account ("/<company_identifier>/accounts" POST)
    def company_decline_account_pass(self, client):
        pass

###TODO: Logout Existing account
    #TODO: Logout pass
    def logout_existing_account_pass(self, client):
        pass

###TODO: Login Created account
    #TODO: Login pass
    def login_created_account_pass(self, client):
        pass

###TODO: Template routes
    #Template empty pass
    def view_all_templates_empty_pass(self, client): #Test when there is no template in company
        response = client.get(f"/templates/{ExistingAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

    def upload_template_filetype_fail(self, client):
        pass

    #TODO: POST add template to company for product creation ("/templates/<company_identifier>" POST) (KYNDA_ADMIN)
        #TODO: Create a folder for template to add
    def upload_template_for_creation_pass(self, client):
        pass

    #TODO: POST add template to company for deletion test ("/templates/<company_identifier>" POST) (KYNDA_ADMIN)
    def upload_template_for_deletion_pass(self, client):
        pass

    #GET view all templates from company ("/templates/<company_identifier>" GET)
    def view_all_templates_exists_pass(self, client): #Test when there are template(s) in company
        response = client.get(f"/templates/{ExistingAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response
        
    #TODO: GET view specific template ("/template/<int:company_identifier>/<int:template_identifier>" GET)
    def view_specific_template_exists_pass(self, client):
        pass
    #TODO: DELETE specific template ("/template/<int:company_identifier>/<int:template_identifier>" DELETE)
    def delete_specific_template_exists_pass(self, client):
        pass

###TODO: Product routes
    #TODO: POST add product to company ("/products/<company_identifier>" POST) (COMPANY_ADMIN/COMPANY_EMPLOYEE)
    def create_product_pass(self, client):
        pass

    #TODO: PUT alter product from company ("/product/<company_identifier>/<product_identifier" PUT) (COMPANY_ADMIN/COMPANY_EMPLOYEE)
    def alter_product_pass(self, client):
        pass

    #TODO: VERIFY PRODUCT (FIRST LOG OUT OF CREATED ACCOUNT, LOG BACK IN TO ADMIN ACCOUNT, VERIFY TESTS, LOG BACK OUT AND IN)
    #TODO: DOWNLOAD PRODUCT

    #TODO: DELETE remove product from company ("/product/<company_identifier>/<product_identifier" DELETE) (COMPANY_ADMIN/COMPANY_EMPLOYEE)    
    def delete_product_pass(self, client):
        pass


###TODO: Image routes
    #TODO: GET view all images of gallery ("/gallery/<company_identifier>/<gallery_identifier>" GET)
    def view_all_images_empty_pass(self, client):
        pass

    #TODO: POST try to add a file with the wrong filetype ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    def upload_image_filetype_fail(self, client):
        pass

    #TODO: POST add an image to delete ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    def upload_image_pass(self, client):
        pass

    #TODO: GET view the selected images from gallery ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" GET)
    def view_specific_image_pass(self, client):
        pass


    #TODO: DELETE remove the image to be deleted ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" DELETE)
    def remove_specific_image_pass(self, client):
        pass

###TODO: Logout Created account
    #TODO: Logout pass
    def logout_created_account_pass(self, client):
        pass

###TODO: Security tests after logging out
        #TODO: TEST Company routes
    def company_route_security_test2(self, client):
        pass

    #TODO: TEST Template routes
    def template_route_security_test2(self, client):
        pass

    #TODO: TEST Product routes
    def product_route_security_test2(self, client):
        pass

    #TODO: TEST image routes
    def image_route_security_test2(self, client):
        pass

    def tearDown(self):
        os.remove("test_sqlite.db")

if __name__ == "__main__":
    unittest.main()