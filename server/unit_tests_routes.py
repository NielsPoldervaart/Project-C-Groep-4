from werkzeug.wrappers import response
from server import app
import unittest
#import requests
import json
from db_controller import setup_basic_db
from user_verification import verify_user
from database_connection import *
from werkzeug.security import generate_password_hash
import os
from io import BytesIO
from generate_random_path import generate_random_path
from ftp_controller import delete_test_folder_ftp

###Global variables
#Fake User
FakeAccountName = generate_random_path(10, "")
FakeAccountPassword = generate_random_path(10, "")
FakeAccountEmail = generate_random_path(10, "@hr.nl")
FakeAccountCompanyID = 2
FakeAccountRole_id = 1

#Existing User
ExistingAccountName = "admin" #TODO: MAYBE MAKE THIS RANDOM TOO?
ExistingAccountPassword = "KYNDA"
ExistingAccountEmail = "admin@hr.nl"
ExistingAccountCompanyID = 1
ExistingAccountRole_id = 1

#Throwaway account
ThrowawayAccountName = generate_random_path(10, "")
ThrowawayAccountPassword = generate_random_path(10, "")
ThrowawayAccountEmail = generate_random_path(10, "@hr.nl")
ThrowawayAccountCompanyID = 1
ThrowawayAccountRole_id = 2

#Created account
CreatedAccountName = generate_random_path(10, "")
CreatedAccountPassword = generate_random_path(10, "")
CreatedAccountEmail = generate_random_path(10, "@hr.nl")
CreatedAccountCompanyID = 1
CreatedAccountRole_id = 1

#Test image and template location
TestImage = "database/gallery/Appa.jpg"
TestTemplate = "database/templates/template1.html"
AdjustedProduct = "database/templates/template2.html"

tester = None

class TestRoutes(unittest.TestCase):
###Database creation
    #Database initialization

    def setUp(self):
        pass

    def test_routes(self):
        #SETTING UP THE DATABASE
        with app.test_client() as client:
            with app.app_context():
                setup_basic_db()
            client.get("/") #Create a session by requesting index route

            #SECURITY TESTS BEFORE LOGGING IN
            # self.company_route_security_tests(client)
            # self.template_route_security_tests(client)
            # self.product_route_security_tests(client)
            # self.image_route_security_tests(client)

            #LOGIN EXISTING ACCOUNT
            # self.login_fail_tests(client)
            self.login_pass(client) #REQUIRED

            #REGISTER NEW ACCOUNTS
            self.register_throwaway_account_pass(client) #REQUIRED
            self.register_actual_account_pass(client) #REQUIRED
            # self.register_account_fail(client)

            #COMPANY ROUTES
            # self.company_info_pass(client)
            # self.company_accounts_info_pass(client)
            # self.company_add_manual_pass(client)
            # self.company_view_manual_pass(client)
            self.company_accept_account_pass(client) #REQUIRED
            # self.company_decline_account_pass(client)

            #LOGOUT EXISTING ACCOUNT
            self.logout_account(client) #REQUIRED

            #LOGIN CREATED ACCOUNT
            self.login_created_account_pass(client) #REQUIRED

            #TEMPLATE ROUTES
            # self.view_all_templates_empty_pass(client)
            # self.upload_template_filetype_fail(client)
            self.upload_template_for_creation_pass(client) #REQUIRED (Product)
            # self.upload_template_for_deletion_pass(client)
            # self.view_all_templates_exists_pass(client)
            # self.view_specific_template_exists_pass(client)
            # self.delete_specific_template_exists_pass(client)

            #PRODUCT ROUTES
            self.create_product_pass(client)
            self.alter_product_pass(client)
            #TODO: Verify product
            self.download_product_pass(client)
            self.delete_product_pass(client)

            #IMAGE ROUTES
            # self.view_all_images_empty_pass(client)
            # self.upload_image_filetype_fail(client)
            # self.upload_image_pass(client)
            # self.view_all_images_exists_pass(client)
            # self.view_specific_image_pass(client)
            # self.remove_specific_image_pass(client)

            #LOGOUT CREATED ACCOUNT
            self.logout_account(client) #REQUIRED

            #SECURITY TESTS AFTER LOGGING OUT
            # self.company_route_security_tests(client)
            # self.template_route_security_tests(client)
            # self.product_route_security_tests(client)
            # self.image_route_security_tests(client)

    def create_db_and_insert_values(self): #CREATES DATABASE FILE + STRUCTURE AND INSERTS NECESSARY VALUES
        init_db_structure()
        with create_db_session() as db_session:
            db_session.add(Role(None, "KYNDA_ADMIN"))
            db_session.add(Role(None, "COMPANY_ADMIN"))
            db_session.add(Role(None, "COMPANY_EMPLOYEE"))
            db_session.add(Gallery(None, "Kynda_gallery"))
            db_session.add(Company(None, "Kynda", 1, None))
            db_session.add(User(None, ExistingAccountName, generate_password_hash(ExistingAccountEmail), generate_password_hash(ExistingAccountPassword), True, ExistingAccountCompanyID, ExistingAccountRole_id))
            db_session.commit()

###Security tests before logging in
    #TESTS Company routes
    def company_route_security_tests(self, client):
        test1 = client.get("/company/1").status_code
        self.assertEqual(test1, 401)

        test2 = client.get("/1/accounts").status_code
        self.assertEqual(test2, 401)

        test3 = client.post("/1/accounts", data={"user_id" : 1, "accepted" : True} ).status_code
        self.assertEqual(test3, 401)

        test4 = client.get("/1/manual").status_code
        self.assertEqual(test4, 401)

        test5 = client.post("/1/manual", data = {"manual_file" : None}).status_code #TODO: Add file to this request
        self.assertEqual(test5, 401)

    #TESTS Template routes
    def template_route_security_tests(self, client):
        test1 = client.get("/templates/1").status_code
        self.assertEqual(test1, 401)
        with open(f'{TestTemplate}', 'rb') as template:
            test2 = client.post(f"/templates/{CreatedAccountCompanyID}", data={'template_file': (template, 'test.txt')}).status_code
        self.assertEqual(test2, 401)

        test3 = client.get("/template/1/1").status_code
        self.assertEqual(test3, 401)

        test4 = client.delete("template/1/1").status_code
        self.assertEqual(test4, 401)

    #TESTS Product routes
    def product_route_security_tests(self, client):
        test1 = client.get("/products/1").status_code
        self.assertEqual(test1, 401)

        test2 = client.post("/products/1", data = {"template_id" : 1}).status_code
        self.assertEqual(test2, 401)

        test3 = client.get("/product/1/1").status_code
        self.assertEqual(test3, 401)

        test4 = client.put("/product/1/1", data = {"updated_product" : None}).status_code #TODO: Add file to this request
        self.assertEqual(test4, 401)

        test5 = client.delete("/product/1/1").status_code
        self.assertEqual(test5, 401)

    #TESTS image routes
    def image_route_security_tests(self, client):
        test1 = client.get("/gallery/1/1").status_code
        self.assertEqual(test1, 401)

        test2 = client.post("/gallery/1/1", data = {"File[]" : None}).status_code #TODO: Add files to this request
        self.assertEqual(test2, 401)

        test3 = client.get("/gallery/1/1/1").status_code
        self.assertEqual(test3, 401)

        test4 = client.delete("/gallery/1/1/1").status_code
        self.assertEqual(test4, 401)

###Login Existing account
    #POST Login fail ALL
    def login_fail_tests(self, client):
        login_fail_all = client.post("/login", json={"name":FakeAccountName, "password":FakeAccountPassword}).status_code
        self.assertEqual(login_fail_all, 406)

        login_fail_password = client.post("/login", json={"name":ExistingAccountName, "password":FakeAccountPassword}).status_code
        self.assertEqual(login_fail_password, 406)

        login_fail_username = client.post("/login", json={"name":FakeAccountName, "password":ExistingAccountPassword}).status_code
        self.assertEqual(login_fail_username, 406)

    #POST Login pass
    def login_pass(self, client):
        response = client.post("/login", json={"name": ExistingAccountName, "password": ExistingAccountPassword})
        test = response.status_code
        self.assertEqual(test, 200)
        return response

###Register new accounts
    #Register throwaway account (verification should get declined)

    def register_account_fail(self, client):
        #Register an account to non existing company
        response = client.post(f"/register/{FakeAccountCompanyID}", data={"name": FakeAccountName, "email" : FakeAccountEmail, "password": FakeAccountPassword, "role_id" : FakeAccountRole_id})
        test = response.status_code
        self.assertEqual(test, 404)
        return response

    def register_throwaway_account_pass(self, client):
        response = client.post(f"/register/{ThrowawayAccountCompanyID}", data={"name": ThrowawayAccountName, "email" : ThrowawayAccountEmail, "password": ThrowawayAccountPassword, "role_id" : ThrowawayAccountRole_id})
        test = response.status_code
        self.assertEqual(test, 201)
        return response

    #TODO: Register actual account (verification should get accepted)
    def register_actual_account_pass(self, client):
        response = client.post(f"/register/{CreatedAccountCompanyID}", data={"name": CreatedAccountName, "email" : CreatedAccountEmail, "password": CreatedAccountPassword, "role_id" : CreatedAccountRole_id})
        test = response.status_code
        self.assertEqual(test, 201)
        return response

###Company routes (View all accounts)
    #GET view company info pass ("/company/<company_identifier>" GET)
    def company_info_pass(self, client):
        test1 = client.get(f"/company/{ExistingAccountCompanyID}").status_code
        self.assertEqual(test1, 200)

    #TODO: GET view company accounts info pass ("/<company_identifier>/accounts" GET)
    def company_accounts_info_pass(self, client):
        test1 = client.get(f"/{ExistingAccountCompanyID}/accounts").status_code
        self.assertEqual(test1, 200)

    #TODO: POST Insert a company manual ("/<company_identifier>/manual" POST)
    def company_add_manual_pass(self, client):
        with open(f'{TestTemplate}', 'rb') as manual: #TODO: MAYBE ADD AN ACTUAL MANUAL FILE
            test1 = client.post(f"/{CreatedAccountCompanyID}/manual", data={'manual_file': (manual, 'test.html')}).status_code
        self.assertEqual(test1, 201)

    #TODO: GET view company manual ("/<company_identifier>/manual" GET)
    def company_view_manual_pass(self, client):
        test1 = client.get(f"/{ExistingAccountCompanyID}/manual").status_code
        self.assertEqual(test1, 200)

    #TODO: POST decline throwaway account ("/<company_identifier>/accounts" POST)
    def company_accept_account_pass(self, client):
        response = client.post(f"/{ExistingAccountCompanyID}/accounts", data = {"user_id" : 3, "accepted" : True}).status_code #TODO: FIND WAY TO FIND CREATED USER ID
        self.assertEqual(response, 201)
        return response

    #TODO: POST verify newly made account ("/<company_identifier>/accounts" POST)
    def company_decline_account_pass(self, client):
        response = client.post(f"/{ExistingAccountCompanyID}/accounts", data = {"user_id" : 2, "accepted" : False}).status_code #TODO: FIND WAY TO FIND CREATED USER ID
        self.assertEqual(response, 201)
        return response

###Logout account
    # Logout pass
    def logout_account(self, client):
        response = client.get("/logout").status_code
        self.assertEqual(response, 201)
        return response

###Login Created account
    #Login pass
    def login_created_account_pass(self, client):
        response = client.post("/login", json={"name": CreatedAccountName, "password": CreatedAccountPassword}).status_code
        self.assertEqual(response, 200)
        return response

###Template routes
    #GET try to view all templates from empty company ("/templates/<company_identifier>" GET)
    def view_all_templates_empty_pass(self, client): #Test when there is no template in company
        response = client.get(f"/templates/{CreatedAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

    #POST try to add template to company with wrong filetype ("/templates/<company_identifier>" POST) (KYNDA_ADMIN)
    def upload_template_filetype_fail(self, client):
        with open(f'{TestTemplate}', 'rb') as template:
            response = client.post(f"/templates/{CreatedAccountCompanyID}", content_type='multipart/form-data', data={'template_file': (template, 'test.txt')})
        statuscode = response.status_code
        self.assertEqual(statuscode, 405)
        return response

    #POST add template to company for product creation ("/templates/<company_identifier>" POST) (KYNDA_ADMIN)
    def upload_template_for_creation_pass(self, client):
        with open(f'{TestTemplate}', 'rb') as template:
            response = client.post(f"/templates/{CreatedAccountCompanyID}", content_type='multipart/form-data', data={'template_file': (template, 'template1.html')})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

    #POST add template to company for deletion test ("/templates/<company_identifier>" POST) (KYNDA_ADMIN)
    def upload_template_for_deletion_pass(self, client):
        with open(f'{TestTemplate}', 'rb') as template:
            response = client.post(f"/templates/{CreatedAccountCompanyID}", content_type='multipart/form-data', data={'template_file': (template, 'template2.html')})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

    #GET view all templates from company ("/templates/<company_identifier>" GET)
    def view_all_templates_exists_pass(self, client): #Test when there are template(s) in company
        response = client.get(f"/templates/{CreatedAccountCompanyID}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response
        
    #GET view specific template ("/template/<int:company_identifier>/<int:template_identifier>" GET)
    def view_specific_template_exists_pass(self, client):
        response = client.get(f"/template/{CreatedAccountCompanyID}/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

    #DELETE specific template ("/template/<int:company_identifier>/<int:template_identifier>" DELETE)
    def delete_specific_template_exists_pass(self, client):
        response = client.delete(f"/template/{CreatedAccountCompanyID}/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

###TODO: Product routes
    #POST add product to company ("/products/<company_identifier>" POST) (COMPANY_ADMIN/COMPANY_EMPLOYEE)
    def create_product_pass(self, client):
        response = client.post(f"/products/{ExistingAccountCompanyID}", data={"template_id": 1})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

    #PUT alter product from company ("/product/<company_identifier>/<product_identifier" PUT) (COMPANY_ADMIN/COMPANY_EMPLOYEE)
    def alter_product_pass(self, client):
        with open(f'{AdjustedProduct}', 'rb') as product:
            response = client.put(f"/product/{CreatedAccountCompanyID}/1", content_type='multipart/form-data', data={'updated_product': (product, 'template1.html')})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

    #TODO: VERIFY PRODUCT (FIRST LOG OUT OF CREATED ACCOUNT, LOG BACK IN TO ADMIN ACCOUNT, VERIFY TESTS, LOG BACK OUT AND IN)
    
    #TODO: POST increase downloads of product ("/product/download/<company_identifier>/<product_identifier" POST)
    def download_product_pass(self,client):
        response = client.put(f"/product/download/{ExistingAccountCompanyID}/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 402) #TODO: change to 201 after verify product implemented
        return response

    #DELETE remove product from company ("/product/<company_identifier>/<product_identifier" DELETE) (COMPANY_ADMIN/COMPANY_EMPLOYEE)    
    def delete_product_pass(self, client):
        response = client.delete(f"/product/{ExistingAccountCompanyID}/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

###Image routes
    #GET try to view all images of empty gallery ("/gallery/<company_identifier>/<gallery_identifier>" GET)
    def view_all_images_empty_pass(self, client):
        response = client.get(f"/gallery/{ExistingAccountCompanyID}/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        return response

    #POST try to add a file with the wrong filetype ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    def upload_image_filetype_fail(self, client):
        with open(f'{TestImage}', 'rb') as image:
            img_tuple = (BytesIO(image.read()), 'test.txt')
        response = client.post(f"/gallery/{ExistingAccountCompanyID}/1", content_type='multipart/form-data', data={'file[]': img_tuple})
        statuscode = response.status_code
        self.assertEqual(statuscode, 405)
        return response

    #POST add an image to delete ("/gallery/<company_identifier>/<gallery_identifier>" POST)
    def upload_image_pass(self, client):
        with open(f'{TestImage}', 'rb') as image:
            img_tuple = (BytesIO(image.read()), 'Appa.jpg')
        response = client.post(f"/gallery/{ExistingAccountCompanyID}/1", content_type='multipart/form-data', data={'file[]': img_tuple})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response

    #GET view all images of gallery ("/gallery/<company_identifier>/<gallery_identifier>" GET)
    def view_all_images_exists_pass(self, client):
        response = client.get(f"/gallery/{ExistingAccountCompanyID}/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response

    #GET view the selected images from gallery ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" GET)
    def view_specific_image_pass(self, client):
        response = client.get(f"gallery/{ExistingAccountCompanyID}/1/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        return response


    #DELETE remove the image to be deleted ("/gallery/<company_identifier>/<gallery_identifier>/<image_identifier>" DELETE)
    def remove_specific_image_pass(self, client):
        response = client.delete(f"gallery/{ExistingAccountCompanyID}/1/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        return response


    def tearDown(self):
        os.remove("test_sqlite.db")
        delete_test_folder_ftp()

if __name__ == "__main__":
    unittest.main()