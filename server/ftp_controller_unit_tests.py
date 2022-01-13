from server import app
from werkzeug.security import generate_password_hash
import unittest
from database_connection import *
from user_verification import verify_user
import os
from io import BytesIO
from ftp_controller import try_to_get_file_ftps_binary, try_to_get_image_ftps, try_to_copy_template_to_product, try_to_upload_file_ftps, delete_test_folder_ftp, try_to_delete_file_ftps

#Company_id to use
CompanyID = 1
TemplatePath = ""
TemplatePath2 = r"database\templates\template2.html"
ImagePath = ""
ImagePath2 = r"database\gallery\Appa.jpg"

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
            #self.
            self.upload_template_test_file_fail()
            self.upload_template_test_ext_fail()
            self.upload_template_test_pass()
            self.retrieve_template_test_pass()
            self.remove_template_test_pass()



###RETRIEVE TESTS (FTP HAS NO CONTENT)
    #TRY TO RETRIEVE TEMPLATE WHEN THERES NOTHING IN FTP
    def retrieve_template_test_fail(self):
        test = try_to_get_file_ftps_binary("fake_template.html", "templates", CompanyID)
        expected_result = ({'Message': 'Test folder does not exist on FTP server', 'errorCode': 404}, 404)
        self.assertEqual(test, expected_result)

    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    def retrieve_product_test_fail(self):
        pass

    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    def retrieve_image_test_fail(self):
        pass

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
        test = try_to_upload_file_ftps(TemplatePath2, "test.html", "templates", CompanyID)
        expected_result = 'PASSED'
        self.assertEqual(test, expected_result)

    #MAKE PRODUCT
    def create_product_test_wrong_template_fail(self):
        pass

    #MAKE PRODUCT
    def create_product_test_pass(self):
        pass

    #SEND IMAGE TO SERVER
    def upload_image_test_pass(self):
        pass

###RETRIEVE TESTS (FTP HAS CONTENT)
    def retrieve_template_test_pass(self):
        test = try_to_get_file_ftps_binary("test.html", "templates", CompanyID)
        expected_result = BytesIO
        self.assertEqual(type(test), expected_result)

    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    def retrieve_product_test_pass(self):
        pass

    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    def retrieve_image_test_pass(self):
        pass

###REMOVE TESTS
    #REMOVE TEMPLATE
    def remove_template_test_pass(self):
        test = try_to_delete_file_ftps("test.html", "templates", CompanyID)
        expected_result = 'PASSED'
        self.assertEqual(test, expected_result)

    #REMOVE PRODUCT
    def remove_product_test_pass(self):
        pass

    #REMOVE IMAGE
    def remove_image_test_pass(self):
        pass

    #DELETE TEST FOLDER
    def remove_test_folder(self):
        pass


    def tearDown(self):
        delete_test_folder_ftp()
        os.remove("test_sqlite.db")

if __name__ == "__main__":
    unittest.main()