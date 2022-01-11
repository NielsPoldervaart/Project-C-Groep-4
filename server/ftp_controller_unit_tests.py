from server import app
from werkzeug.security import generate_password_hash
import unittest
from database_connection import *
from user_verification import verify_user
import os
from ftp_controller import try_to_get_file_ftps_binary, get_image, try_to_copy_template_to_product, upload_file, delete_test_folder_ftp

#Company_id to use
CompanyID = 1

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

    #CREATE TEST FOLDER

    #TRY TO RETRIEVE TEMPLATE WHEN THERES NOTHING IN FTP
    def retrieve_template_test_fail(self):
        test = try_to_get_file_ftps_binary("fake_template.html", "templates", CompanyID)
        expected_result = ({"errorCode": 404, "Message": "Test folder does not exist on FTP server"}, 404)
        self.assertEqual(test, expected_result)

    #TRY TO RETRIEVE PRODUCT WHEN THERES NOTHING IN FTP
    def retrieve_product_test_fail(self, client):
        pass

    #TRY TO RETRIEVE IMAGE WHEN THERES NOTHING IN FTP
    def retrieve_image_test_fail(self, client):
        pass

    #SEND TEMPLATE TO SERVER
    def upload_template_tests(self, client):
        def upload_template_test_fail(self, client): #UPLOAD TEMPLATE FAIL (NO TEMPLATE PROVIDED)
            pass

        def upload_template_test_pass(self, client): #UPLOAD TEMPLATE PASS ()
            pass

    #MAKE PRODUCT
    def create_product_test_pass(self, client):
        pass

    #SEND IMAGE TO SERVER
    def upload_image_test_pass(self, client):
        pass

    #REMOVE TEMPLATE
    def remove_template_test_pass(self, client):
        pass

    #REMOVE PRODUCT
    def remove_product_test_pass(self, client):
        pass

    #REMOVE IMAGE
    def remove_image_test_pass(self, client):
        pass

    #DELETE TEST FOLDER
    def remove_test_folder(self, client):
        pass


    def tearDown(self):
        os.remove("test_sqlite.db")

if __name__ == "__main__":
    unittest.main()