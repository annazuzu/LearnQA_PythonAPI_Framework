import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        responce = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(responce, "username")
        Assertions.assert_json_has_not_key(responce, "firstName")
        Assertions.assert_json_has_not_key(responce, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(responce1, "user_id")

        responce2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(responce2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(responce1, "user_id")

        # Проверим, авторизованы ли мы?
        responce2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # Возьмем другого пользователя:
        responce3 = requests.get(f"https://playground.learnqa.ru/api/user/1")

        # Сделаем три проверки:
        # 1 - на наличие поля "username",
        # 2 - на то, что возвращается определенное значение в этом поле,
        # 3 - на то, что остальные поля, которые возвращаются только авторизованному пользователю, нам не вернулись.

        Assertions.assert_json_has_key(responce3, "username")
        u_name = self.get_json_value(responce3, "username")
        Assertions.assert_json_value_by_name(responce3, "username", u_name, f"This {u_name} doesn't exist")

        not_expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce3, not_expected_fields)
