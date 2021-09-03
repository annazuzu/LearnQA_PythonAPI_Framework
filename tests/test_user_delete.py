import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_user_delete_id_2(self):
        # Авторизуемся:

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        # Проверяем авторизацию:
        responce2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # Попытаемся удалить:

        responce3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )

        # Проверим удалился ли:

        responce4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_has_key(responce4, "username")
        Assertions.assert_json_has_keys(responce4, expected_fields)

    def test_user_create_and_delete(self):
        # 1. Создание:

        data = self.prepare_registration_data()
        responce = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(responce, 200)
        Assertions.assert_json_has_key(responce, "id")

        email = data['email']
        password = data['password']
        user_id = self.get_json_value(responce, "id")

        # 2. Авторизация:

        data_for_registration = {
            'email': email,
            'password': password
        }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data_for_registration)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        print(f"Юзер айди свежесозданного пользователя: {user_id_auth}")

        # 3. Проверка авторизации:
        responce2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # 4. Удаление:

        responce3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )

        Assertions.assert_code_status(responce3, 200)

        # 5. Проверка удаления:

        responce4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(responce4, 404)
        # Проверка должна упасть и падает!!!  AssertionError: Responce is not JSON format. Responce text is 'User not found'
        Assertions.assert_json_has_key(responce4, "username")

    def test_delete_not_that_user(self):
        # 1. Создадим нового пользователя:

        data = self.prepare_registration_data()
        responce = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(responce, 200)
        Assertions.assert_json_has_key(responce, "id")

        email = data['email']
        password = data['password']
        user_id = self.get_json_value(responce, "id")

        # 2. И авторизуемся под ним:

        data_for_registration = {
            'email': email,
            'password': password
        }

        responce1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data_for_registration)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        print(f"Юзер айди свежесозданного пользователя: {user_id_auth}")

        # 3. Пройдем проверку на авторизацию:

        responce2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # 4. Попытаемся удалить старого пользователя с id=9196:

        user_id_old = '9196'

        responce3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_old}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )

        Assertions.assert_code_status(responce3, 200)

        # 5. Проверим удалился ли?:

        responce4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_old}")

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_has_key(responce4, "username")
        keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce4, keys)
