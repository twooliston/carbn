from app import app
import unittest

from carbn_app.extensions import db

from carbn_app.Models.Customer import Customer

# TODO: implement logger


class ExampleTest(unittest.TestCase):

    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/customer")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # check if content returned is application/json
    def test_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/customer")
        self.assertEqual(response.content_type, "application/json")

    # check returned data (with no saved data)
    def test_returned_data(self):
        tester = app.test_client(self)
        response = tester.get("/customer")
        self.assertTrue(b'[]' in response.data)


if __name__ == "__main__":
    unittest.main()
