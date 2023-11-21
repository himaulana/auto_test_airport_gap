import os
import requests
from assertpy import assert_that
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class TestFavorite:
    URL = 'https://airportgap.com/api/favorites'
    TOKEN = 'RhxPc3RmfBjKktwahe2Bj8Jn'

    @property
    def __body_favorite(self):
        body = {
            'airport_id': 'GKA',
            'note': 'This is favorite airport with him'
        }
        return body

    def __get_first_data_favorite(self):
        headers = {"Authorization": f"Token {self.TOKEN}"}
        response = requests.get(self.URL, headers=headers)
        data = response.json().get('data')[0]
        favorite = {
            'id': data.get('id'),
            'name': data.get('attributes').get('airport').get('name')
        }

        return favorite

    def test_create_favorite_airport(self):
        headers = {"Authorization": f"Bearer token={self.TOKEN}"}
        response = requests.post(self.URL, data=self.__body_favorite, headers=headers)

        data = response.json().get('data')
        airport = data.get('attributes').get('airport')

        assert_that(response.status_code).is_equal_to(201)
        assert_that(data).is_instance_of(dict)
        assert_that(data.get('type')).is_equal_to('favorite')
        assert_that(airport['name']).is_equal_to('Goroka Airport')
        assert_that(airport['country']).is_equal_to_ignoring_case('Papua New GuineA')

    def test_get_favorite_airport(self):
        headers = {"Authorization": f"Token {self.TOKEN}"}
        response = requests.get(self.URL, headers=headers)

        data = response.json().get('data')
        attributes = data[0]['attributes']
        body = self.__body_favorite

        assert_that(response.status_code).is_equal_to(200)
        assert_that(data).is_not_empty()
        assert_that(data).is_instance_of(list)
        assert_that(len(data)).is_greater_than_or_equal_to(1)
        assert_that(attributes.get('note')).is_equal_to(body.get('note'))

    def test_patch_favorite_airport(self):
        favorite = self.__get_first_data_favorite()
        body_created = self.__body_favorite

        headers = {"Authorization": f"Bearer token={self.TOKEN}"}
        body = {'note': 'But he was gone... Nice Try gueys'}
        response = requests.patch(self.URL + f'/{favorite.get("id")}', data=body, headers=headers)

        data = response.json().get('data')

        assert_that(response.status_code).is_equal_to(200)
        assert_that(data).is_instance_of(dict)
        assert_that(data.get('id')).is_equal_to(favorite.get('id'))
        assert_that(data.get('attributes').get('airport').get('name')).is_equal_to(favorite.get('name'))
        assert_that(data.get('attributes').get('note')).is_not_equal_to(body_created.get('note'))

    def test_delete_favorite_airport(self):
        favorite = self.__get_first_data_favorite()
        headers = {"Authorization": f"Bearer token={self.TOKEN}"}

        response = requests.delete(self.URL + f'/{favorite.get("id")}', headers=headers)

        assert_that(response.status_code).is_equal_to(204)
