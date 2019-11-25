import os
import unittest

from flask_testing import TestCase

from app import create_app


class BaseTestCase(TestCase):
    """ Base Test Class """

    def create_app(self):
        os.environ['APP_SETTINGS'] = 'config.TestConfig'
        app = create_app()
        return app


class AviaFlightsCase(BaseTestCase):
    def test_api(self):
        response = self.client.get(
            "/api/v1/routes/?source=DXB&destination=BKK",
        )
        self.assertEqual(response.status_code, 200)

    def test_sort_api(self):
        response = self.client.get(
            "/api/v1/routes/?source=DXB&destination=BKK&sort=fastest",
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
