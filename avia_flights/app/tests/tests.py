import os
import unittest

from flask_testing import TestCase
from flask import url_for

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
            url_for('main.search_routes', source='DXB', destination='BKK')
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(312, len(response.json))

    def test_sort_api(self):
        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='fastest'
            )
        )
        self.assertStatus(response, 200)
        self.assertTrue(isinstance(response.json, dict))

        eq_d = {
            'onward_itinerary': [{
                'arrival_time_stamp': 'Sun, 28 Oct 2018 00:20:00 GMT',
                'carrier': 'Emirates', 'class_number': 'U',
                'departure_time_stamp': 'Sat, 27 Oct 2018 15:20:00 GMT',
                'destination': 'BKK',
                'fare_basis': '\n2820303decf751-5511-447a-aeb1-810a6b10ad7'
                              'd@@$255_DXB_BKK_370_32_15:20__A2_1_1\n',
                'flight_number': 370, 'number_of_stops': 0,
                'source': 'DXB',
                'ticket_type': 'E', 'warning_text': ''
            }],
            'pricing': {
                'single_adult': {'airline_taxes': 290.7, 'base_fare': 521.0,
                                 'total_amount': 811.7},
                'single_child': {'airline_taxes': 290.7, 'base_fare': 393.0,
                                 'total_amount': 683.7},
                'single_infant': {'airline_taxes': None, 'base_fare': 55.0,
                                  'total_amount': 55.0}
            },
            'request_datetime': ['Mon, 28 Sep 2015 20:30:26 GMT'],
            'return_itinerary': None
        }

        self.assertDictEqual(eq_d, response.json['0'])

        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='fastest',
                limit=3
            )
        )
        self.assertStatus(response, 200)
        self.assertEqual(3, len(response.json))

        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='slowest',
            )
        )
        self.assertStatus(response, 200)
        self.assertEqual(1, len(response.json))

        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='cheapest',
            )
        )
        self.assertStatus(response, 200)
        self.assertEqual(1, len(response.json))

        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='expensive',
            )
        )
        self.assertStatus(response, 200)
        self.assertEqual(1, len(response.json))

        response = self.client.get(
            url_for(
                'main.search_routes',
                source='DXB',
                destination='BKK',
                sort='optimal',
            )
        )
        self.assertStatus(response, 200)
        self.assertEqual(1, len(response.json))

    def test_diff(self):
        response = self.client.get(
            url_for('main.diff_request')
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(172, len(response.json))


if __name__ == "__main__":
    unittest.main(verbosity=2)
