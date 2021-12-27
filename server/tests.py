from server import app
import unittest
#import requests
import json

class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        data = {"name" : "ADMIN@hr.nl", "password" : "KYNDA"}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = tester.post("/login", data= json.dumps(data), headers = headers)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


if __name__ == "__main__":
    unittest.main()