from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # 1.	Создание пользователя:

        register_data = self.prepare_registration_data()
        responce1 = MyRequests.post("/user/", data=register_data)

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

        responce2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(responce2, "auth_sid")
        token = self.get_header(responce2, "x-csrf-token")

        # 3.	Редактирование данных:

        new_name = "Changed name"

        responce3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        # Проверочки:
        Assertions.assert_code_status(responce3, 200)

        # 4.	Получение данных пользователя и сравнение имени с новым:

        responce4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_json_value_by_name(responce4, "firstName", new_name, "Wrong name of the user after edit")

    # Изменить данные пользователя, будучи неавторизованными:
    def test_edit_not_auth_user(self):
        # Возьмем старого пользователя с id=9196:

        user_id_old = '9196'
        new_name = "Changed name for 9196"

        # Попытаемся изменить ему имя передав только data:

        responce = MyRequests.put(f"/user/{user_id_old}",
                                  data={"username": new_name}
                                  )

        Assertions.assert_code_status(responce, 400)

        # А теперь попытаемся передать полный набор параметров, но токен и auth_sid будут фейковыми, так как пользователь не ввел логин и пароль:

        responce1 = MyRequests.put(f"/user/{user_id_old}",
                                   headers={"x-csrf-token": "1"},
                                   cookies={"auth_sid": "1"},
                                   data={"username": new_name}
                                   )
        Assertions.assert_code_status(responce1, 400)

        # Проверим изменилось ли его имя:
        responce2 = MyRequests.get(f"/user/{user_id_old}",
                                   headers={"x-csrf-token": "1"},
                                   cookies={"auth_sid": "1"},
                                   )

        Assertions.assert_code_status(responce2, 200)
        Assertions.assert_json_has_key(responce2, "username")
        keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce2, keys)
        Assertions.assert_json_value_by_name_negative(responce2, "username", new_name,
                                                      "Wrong name of the user after edit")

        # Оба запроса отработали со статус-кодом 400, имя пользователя таким способом поменять нельзя.

    # Изменить данные пользователя, будучи авторизованными другим пользователем:

    def test_edit_not_that_user(self):
        # 1.	Создание пользователя:

        register_data = self.prepare_registration_data()
        responce1 = MyRequests.post("/user/", data=register_data)

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

        responce2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(responce2, "auth_sid")
        token = self.get_header(responce2, "x-csrf-token")

        # 3. А вот отредактируем старого пользователя с id=9196:

        user_id_old = '9196'
        new_name = "Changed name for 9196"

        responce3 = MyRequests.put(f"/user/{user_id_old}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"username": new_name},
                                   )

        Assertions.assert_code_status(responce3, 200)

        # 4.	Получение данных пользователя и сравнение имени с новым:

        responce4 = MyRequests.get(f"/user/{user_id_old}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_has_key(responce4, "username")
        keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce4, keys)
        Assertions.assert_json_value_by_name_negative(responce4, "username", new_name,
                                                      "Wrong name of the user after edit")

        # Несмотря на то, что запрос на изменение отработал со статусом 200, данные не поменялись. Значит таким
        # способом изменять данные тоже нельзя.

    # Изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @:

    def test_edit_created_user_wrong_email(self):
        # 1.	Создание пользователя:

        register_data = self.prepare_registration_data()
        responce1 = MyRequests.post("/user/", data=register_data)

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

        responce2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(responce2, "auth_sid")
        token = self.get_header(responce2, "x-csrf-token")

        # 3.	Редактирование данных:

        new_email = "annaexample.com"

        responce3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )

        # Проверочки:
        Assertions.assert_code_status(responce3, 400)
        Assertions.assert_json_value_by_name(responce3, "email", new_email, "This string is not email")
        print(responce3.content.decode('utf-8'))

        # 4.	Получение данных пользователя и сравнение email с новым:

        responce4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(responce4, 200)
        print(responce4.content.decode('utf-8'))
        Assertions.assert_json_value_by_name_negative(responce4, "email", new_email, "Email has been changed")

    # Изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один
    # символ:

    def test_edit_created_user_wrong_firstname(self):
        # 1.	Создание пользователя:

        register_data = self.prepare_registration_data()
        responce1 = MyRequests.post("/user/", data=register_data)

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

        responce2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(responce2, "auth_sid")
        token = self.get_header(responce2, "x-csrf-token")

        # 3.	Редактирование данных:

        new_firstname = "1"

        responce3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_firstname}
                                   )

        # Проверочки:
        Assertions.assert_code_status(responce3, 400)
        Assertions.assert_json_value_by_name(responce3, "error", "Too short value for field firstName",
                                             "Field 'firstName' longer than 1 symbol")

        # 4.	Получение данных пользователя и сравнение firstName с новым:

        responce4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_value_by_name_negative(responce4, "firstName", new_firstname,
                                                      "FirstName has been changed")
