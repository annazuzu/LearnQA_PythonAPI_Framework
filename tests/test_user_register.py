import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_email_without_a(self):
        data = self.prepare_registration_data('annaexample.com')

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, "email", data["email"], "This string is not email")

    def test_create_user_with_short_name(self):
        short_uname = '1'
        data = self.prepare_registration_data_username(short_uname)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_too_long_or_short_name(response, "username", short_uname, "This username have more than 1 symbol")

    def test_create_user_with_long_name(self):
        long_uname = 'XMwbqKozlpFOtWKTMksTsQRRpRLnHrwzeitwyLXngrAZFJucvVRgiMOjdWEZsURWAuMOOvojDvPAlQajjJxgknGNxCujbRqd' + \
                     'GbaneHynFXgNfawMHnYjJeNIPrfszSkQRWGZhMynBgwquCwNSjzCxputlKdSxtOvCUzjmUkvyeHZPaNFzomFhKqyCAgYpdsez'+ \
                     'DthwpHvIrPoDqJuhnZTCQzixenpUkimmsuFcsvoJADeyCzxzYeKekRqiqp'
        data = self.prepare_registration_data_username(long_uname)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_too_long_or_short_name(response, "username", long_uname, "This username have less than 250 symbols")

    testdata = [
        (None, 'learnqa', 'learnqa', 'learnqa', 'anna@example.com'),
        ('123', None, 'learnqa', 'learnqa', 'anna@example.com'),
        ('123', 'learnqa', None, 'learnqa', 'anna@example.com'),
        ('123', 'learnqa', 'learnqa', None, 'anna@example.com'),
        ('123', 'learnqa', 'learnqa', 'learnqa', None)
    ]

    @pytest.mark.parametrize('password, username, first_name, last_name, email', testdata)
    def test_create_user_some_field_empty_param(self, password, username, first_name, last_name, email):
        data = {
            'password': password,
            'username': username,
            'firstName': first_name,
            'lastName': last_name,
            'email': email
        }

        responce = MyRequests.post("/user/", data=data)

        missing_param = self.k_v_data_items(data)

        Assertions.assert_code_status(responce, 400)
        Assertions.assert_json_value_by_name(responce, missing_param, data[missing_param], f"Field '{missing_param}' is not None and have value {data[missing_param]}")

    # Метод для теста, не обращать внимание:

    def test_create_user_some_field_empty(self):
        data = {
            'password': None,
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'anna@example.com'
        }

        response = MyRequests.post("/user/", data=data)

        missing_param = self.k_v_data_items(data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {missing_param}", f"Unexpected response content {response.content}"
