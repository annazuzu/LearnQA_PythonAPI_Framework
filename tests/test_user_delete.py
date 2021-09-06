import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Delete user")
class TestUserDelete(BaseCase):
    @allure.title("Удаление пользователя: негативный тест №1")
    @allure.description("Тест на попытку удалить пользователя по ID 2 (неудаляемый пользователь)")
    def test_user_delete_id_2(self):
        # Авторизуемся:

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        # Проверяем авторизацию:
        responce2 = MyRequests.get(f"/user/{user_id_auth}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # Попытаемся удалить:

        responce3 = MyRequests.delete(f"/user/{user_id_auth}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        # Проверим удалился ли:

        responce4 = MyRequests.get(f"/user/{user_id_auth}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_has_key(responce4, "username")
        Assertions.assert_json_has_keys(responce4, expected_fields)

    @allure.title("Удаление пользователя: позитивный тест")
    @allure.description("Создать пользователя, авторизоваться из-под него, удалить, + проверка, что он удалён")
    def test_user_create_and_delete(self):
        # 1. Создание:

        data = self.prepare_registration_data()
        responce = MyRequests.post("/user/", data=data)

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

        responce1 = MyRequests.post("/user/login", data=data_for_registration)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        print(f"Юзер айди свежесозданного пользователя: {user_id_auth}")

        # 3. Проверка авторизации:
        responce2 = MyRequests.get(f"/user/{user_id_auth}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # 4. Удаление:

        responce3 = MyRequests.delete(f"/user/{user_id_auth}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_code_status(responce3, 200)

        # 5. Проверка удаления:

        responce4 = MyRequests.get(f"/user/{user_id_auth}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(responce4, 404)
        Assertions.assert_user_not_exist(responce4, "User is exist!")

    @allure.title("Удаление пользователя: негативный тест №2")
    @allure.description("Удалить пользователя, будучи авторизованным другим пользователем. ОР: пользователь не удалён")
    def test_delete_not_that_user(self):
        # 1. Создадим нового пользователя:

        data = self.prepare_registration_data()
        responce = MyRequests.post("/user/", data=data)

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

        responce1 = MyRequests.post("/user/login", data=data_for_registration)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_auth = self.get_json_value(responce1, "user_id")

        print(f"Юзер айди свежесозданного пользователя: {user_id_auth}")

        # 3. Пройдем проверку на авторизацию:

        responce2 = MyRequests.get(f"/user/{user_id_auth}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # 4. Попытаемся удалить старого пользователя с id=9196:

        user_id_old = '9196'

        responce3 = MyRequests.delete(f"/user/{user_id_old}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_code_status(responce3, 200)

        # 5. Проверим удалился ли?:

        responce4 = MyRequests.get(f"/user/{user_id_old}")

        Assertions.assert_code_status(responce4, 200)
        Assertions.assert_json_has_key(responce4, "username")
        keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce4, keys)
