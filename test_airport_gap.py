import requests
import os
from assertpy import assert_that
from dotenv import load_dotenv

load_dotenv()

class TestSchedule:
    def test_schedules(self):
        response = requests.get(os.getenv('BASE_URL'))
        data = response.json().get('data')

        self.asserts_response(response)

        assert_that(data).is_type_of(list)
        assert_that(data).is_length(30)
        assert_that(data).is_iterable()

    def test_schedule_detail(self):
        response = requests.get(os.getenv('BASE_URL') + '/' + os.getenv('ONE_SCHEDULE_ID'))
        data = response.json().get('data')
        attributes = data.get('attributes')

        self.asserts_response(response)
        self.asserts_detail(data, attributes)

    def asserts_response(self, response):
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_type_of(dict)
        assert_that(response.json()).is_not_empty()
        assert_that(response.json()).contains_key('data')

    def asserts_detail(self, data, attributes):
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


def test_schedules_not_found():
    response = requests.get(os.getenv('BASE_URL') + 's')
    assert response.status_code == 404

def test_schedule_detail_not_found():
    keys_error = ['status','title','detail']
    response = requests.get(os.getenv('BASE_URL') + '/IKD')
    errors = response.json().get('errors')

    assert response.status_code == 404
    assert 'errors' in response.json()
    assert isinstance(response.json(), dict)
    assert isinstance(errors, list)

    for key in keys_error:
        assert key in errors[0].keys()









response = requests.get(os.getenv('BASE_URL') + '/GKA')
data = response.json().get('data')
print(data)