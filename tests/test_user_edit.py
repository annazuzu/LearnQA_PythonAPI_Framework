import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # 1.	Создание пользователя:

        register_data = self.prepare_registration_data()
        responce1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        # Сервер отвечает кодом ответа 200 и в нем есть id нового пользователя:

        Assertions.assert_code_status(responce1, 200)
        Assertions.assert_json_has_key(responce1, "id")

        email = register_data['email']
        firstname = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(responce1, "id")

        # 2.	Авторизация:

        login_data = {
            'email': email,
            'password': password
        }

        responce2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(responce2, "auth_sid")
        token = self.get_header(responce2, "x-csrf-token")

        # 3.	Редактирование данных:

        new_name = "Changed name"

        responce3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        # Проверочки:
        Assertions.assert_code_status(responce3, 200)

        # 4.	Получение данных пользователя и сравнение имени с новым:

        responce4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_value_by_name(responce4, "firstName", new_name, "Wrong name of the user after edit")
