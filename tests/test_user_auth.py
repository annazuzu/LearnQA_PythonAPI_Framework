import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Первый запрос:
        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.get_cookie(responce1, "auth_sid")
        self.token = self.get_header(responce1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(responce1, "user_id")

    def test_auth_user(self):

        # Второй запрос:

        responce2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            responce2,
            "user_id",
            self.user_id_from_auth_method,
            "User id in auth method is not equal to user id from check method"
        )

    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            responce2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token},

            )
        else:
            responce2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid},
            )

        Assertions.assert_json_value_by_name(
            responce2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
