import requests
import os
from assertpy import assert_that
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class TestSchedule:
    URL = 'https://airportgap.com/api/airports'

    def __general_asserts(self, response):
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_type_of(dict)
        assert_that(response.json()).is_not_empty()
        assert_that(response.json()).contains_key('data')

    def test_schedules(self):
        response = requests.get(self.URL)
        data = response.json().get('data')

        self.__general_asserts(response)

        assert_that(data).is_type_of(list)
        assert_that(data).is_length(30)
        assert_that(data).is_iterable()

    def test_schedule_detail(self):
        response = requests.get(self.URL + '/' + os.getenv('ONE_SCHEDULE_ID'))
        data = response.json().get('data')
        attributes = data.get('attributes')

        self.__general_asserts(response)

        assert_that(data).is_instance_of(dict)
        assert_that(data).is_not_empty()
        assert_that(data).is_length(3)
        assert_that(data).contains_key(*os.getenv('ONE_SCHEDULE_KEYS_DATA').split(','))
        assert_that(data).contains_value(*os.getenv('ONE_SCHEDULE_VALUES_DATA').split(','))

        assert_that(attributes).is_instance_of(dict)
        assert_that(attributes).is_not_empty()
        assert_that(attributes).is_length(9)
        assert_that(attributes).contains_key(*os.getenv('ONE_SCHEDULE_KEYS_ATTRIBUTES').split(','))
        assert_that(attributes).contains_value(*os.getenv('ONE_SCHEDULE_VALUES_ATTRIBUTES').split(','))
        assert_that(attributes.get('name')).is_equal_to(os.getenv('ONE_SCHEDULE_NAME'))
        assert_that(attributes.get('latitude')).is_equal_to(os.getenv('ONE_SCHEDULE_LATITUDE'))
        assert_that(attributes.get('icao')).is_equal_to(os.getenv('ONE_SCHEDULE_ICAO'))

    def test_schedules_not_found(self):
        response = requests.get(self.URL + 's')
        assert_that(response.status_code).is_equal_to(404)

    def test_schedule_detail_not_found(self):
        keys_error = ['status', 'title', 'detail']
        values_error = ['404', 'Not Found', 'The page you requested could not be found']
        response = requests.get(self.URL + '/IKD')
        errors = response.json().get('errors')

        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).is_instance_of(dict)
        assert_that(response.json()).contains('errors')
        assert_that(errors).is_instance_of(list)
        assert_that(errors[0]).is_not_empty()
        assert_that(errors[0]).is_instance_of(dict)
        assert_that(errors[0]).contains_key(*keys_error)
        assert_that(errors[0]).contains_value(*values_error)

