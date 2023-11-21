import os
import requests
from assertpy import assert_that
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class TestDistances:
    URL = 'https://airportgap.com/api/airports'

    def test_calculation(self):
        body = {
            'from': 'KIX',
            'to': 'NRT'
        }
        response = requests.post(self.URL + '/distance', data=body)
        data = response.json().get('data')
        attributes = data.get('attributes')

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_not_empty()
        assert_that(response.json()).is_instance_of(dict)
        assert_that(data).is_instance_of(dict)
        assert_that(data).contains_key('id', 'type', 'attributes')
        assert_that(data.get('id')).is_equal_to(body.get('from') + '-' + body.get('to'))
        assert_that(attributes.get('kilometers')).is_equal_to(490.8053652969214)
        assert_that(attributes.get('miles')).is_equal_to(304.76001022047103)
        assert_that(attributes.get('nautical_miles')).is_equal_to(264.82908133654655)

    def test_calculation_not_found(self):
        body = {
            'from': 'KIX',
            'to': 'JKT'
        }
        keys_error = ['status', 'title', 'detail']
        values_error = ['422', 'Unable to process request', 'Please enter valid \'from\' and \'to\' airports.']

        response = requests.post(self.URL + '/distance', data=body)
        data = response.json().get('errors')

        assert_that(response.status_code).is_equal_to(422)
        assert_that(response.json()).is_instance_of(dict)
        assert_that(response.json()).contains('errors')
        assert_that(data).is_instance_of(list)
        assert_that(data[0]).is_not_empty()
        assert_that(data[0]).is_instance_of(dict)
        assert_that(data[0]).contains_key(*keys_error)
        assert_that(data[0]).contains_value(*values_error)
