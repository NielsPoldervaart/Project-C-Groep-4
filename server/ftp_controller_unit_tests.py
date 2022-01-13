from server import app
from werkzeug.security import generate_password_hash
import unittest
from database_connection import *
from user_verification import verify_user
import os
from ftp_controller import try_to_get_file_ftps_binary, try_to_get_image_ftps, try_to_copy_template_to_product, try_to_upload_file_ftps, delete_test_folder_ftp, try_to_delete_file_ftps
from io import BytesIO

#Company_id to use
CompanyID = 1
TemplatePath = "database/templates/template1.html"
TemplatePath2 = r"database\templates\template2.html"
TemplateName = "template1.html"
ImagePath = "database/gallery/Horse.jpg"
ImagePath2 = r"database\gallery\Appa.jpg"
ImageName = "Horse.jpg"
ProductName = TemplateName

FakeTemplateName = "fake_template.html"
FakeProductName = "fake_product.html"
FakeImageName = "fake_image.jpg"

class Test_user_verification_module(unittest.TestCase):
###Database creation
    #Database initialization
    
    def setUp(self):
        #init_db_structure("sqlite://")
        #setup_basic_db()
        pass
    
    def test_ftp_controller(self):
        with app.test_client() as client:
            client.get("/") #Create a session by requesting index route
            self.retrieve_template_test_fail()
            self.retrieve_product_test_fail()
            self.retrieve_image_test_fail()
            self.upload_template_test_file_fail()
            self.upload_template_test_ext_fail()
            self.upload_template_test_pass()
            self.create_product_test_wrong_template_fail()
            self.create_product_test_pass()
            self.upload_image_test_pass()
            self.retrieve_template_test_pass()
            self.retrieve_product_test_pass()
            self.retrieve_image_test_pass()
            self.remove_template_test_pass()
            self.remove_product_test_pass()
            self.remove_image_test_pass()
            self.remove_test_folder()



###RETRIEVE TESTS (FTP HAS NO CONTENT)
    #TRY TO RETRIEVE TEMPLATE WHEN THERES NOTHING IN FTP
    def retrieve_template_test_fail(self):
        test = try_to_get_file_ftps_binary("fake_template.html", "templates", CompanyID)
        expected_result = ({'Message': 'Test folder does not exist on FTP server', 'errorCode': 404}, 404)
        self.assertEqual(test, expected_result)

    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    def retrieve_product_test_fail(self):
        test = try_to_get_file_ftps_binary(ProductName, "products", CompanyID)
        expected_result = ({"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404)
        self.assertEqual(test, expected_result)

    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    def retrieve_image_test_fail(self):
        test = try_to_get_image_ftps(ImageName, "gallery", CompanyID)
        expected_result = ({"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404)
        self.assertEqual(test, expected_result)

###UPLOAD TESTS
    #TRY UPLOAD TEMPLATE FAIL WITH NO TEMPLATE PROVIDED
    def upload_template_test_file_fail(self):
        test = try_to_upload_file_ftps("", "filename.html", "templates", CompanyID)
        expected_result = ({"errorCode": 404, "Message": "No file found in request"}, 404)
        self.assertEqual(test, expected_result)

    #TRY TO UPLOAD A TEMPLATE WITH WRONG EXTENSION
    def upload_template_test_ext_fail(self): 
        test = try_to_upload_file_ftps(ImagePath2, "test.jpg", "templates", CompanyID)
        expected_result = ({'Message': 'Extension not supported for this type of file', 'errorCode': 404}, 404)
        self.assertEqual(test, expected_result)

    def upload_template_test_pass(self): #UPLOAD TEMPLATE PASS ()
        test = try_to_upload_file_ftps(TemplatePath2, TemplateName, "templates", CompanyID)
        expected_result = 'PASSED'
        self.assertEqual(test, expected_result)

    #MAKE PRODUCT
    def create_product_test_wrong_template_fail(self):
        test = try_to_copy_template_to_product(FakeTemplateName, CompanyID)
        expected_result = ({"errorCode": 404, "Message": "Requested file not found on FTP server"}, 404)
        self.assertEqual(test, expected_result)

    #MAKE PRODUCT
    def create_product_test_pass(self):
        test = try_to_copy_template_to_product(TemplateName, CompanyID)
        expected_result = ({"Code": 201, "Message": "Product succesfully created"}, 201)
        self.assertEqual(test, expected_result)

    #SEND IMAGE TO SERVER
    def upload_image_test_pass(self):
        test = try_to_upload_file_ftps(ImagePath, ImageName, "gallery", CompanyID)
        expected_result = "PASSED"
        self.assertEqual(test, expected_result)

###RETRIEVE TESTS (FTP HAS CONTENT)
    def retrieve_template_test_pass(self):
        test = try_to_get_file_ftps_binary(TemplateName, "templates", CompanyID)
        expected_result = BytesIO
        self.assertEqual(type(test), expected_result)

    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    def retrieve_product_test_pass(self):
        test = try_to_get_file_ftps_binary(ProductName, "products", CompanyID)
        expected_result = BytesIO
        self.assertEqual(type(test), expected_result)

    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    def retrieve_image_test_pass(self):
        test = try_to_get_image_ftps(ImageName, "gallery", CompanyID)
        expected_result = str
        self.assertEqual(type(test), expected_result)

###REMOVE TESTS
    #REMOVE TEMPLATE
    def remove_template_test_pass(self):
        test = try_to_delete_file_ftps(TemplateName, "templates", CompanyID)
        expected_result = 'PASSED'
        self.assertEqual(test, expected_result)

    #REMOVE PRODUCT
    def remove_product_test_pass(self):
        test = try_to_delete_file_ftps(ProductName, "products", CompanyID)
        expected_result = "PASSED"
        self.assertEqual(test, expected_result)

    #REMOVE IMAGE
    def remove_image_test_pass(self):
        test = try_to_delete_file_ftps(ImageName, "gallery", CompanyID)
        expected_result = "PASSED"
        self.assertEqual(test, expected_result)

    #DELETE TEST FOLDER
    def remove_test_folder(self):
        delete_test_folder_ftp()


    def tearDown(self):
        delete_test_folder_ftp()
        os.remove("test_sqlite.db")

if __name__ == "__main__":
    unittest.main()