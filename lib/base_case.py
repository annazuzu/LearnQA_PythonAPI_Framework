import json

from requests import Response
from datetime import datetime

class BaseCase:
    def get_cookie (self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last responce"
        return response.cookies[cookie_name]

    def get_header (self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last responce"
        return response.headers[headers_name]

    def get_json_value (self, response: Response, name):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

        return responce_as_dict[name]

    def prepare_registration_data (self, email=None):
        if email == None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_registration_data_username (self, username=None, email=None):
        if email == None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def k_v_data_items(self, my_dict):
        for key, value in my_dict.items():
            if value is None:
                return key
