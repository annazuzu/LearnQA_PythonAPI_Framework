import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Requesting another user's data")
class TestUserGet(BaseCase):
    @allure.title("Получение данных пользователя: неавторизованный запрос, позитивный тест")
    @allure.description("Неавторизованный запрос на данные. ОР: в ответе только 'username'")
    def test_get_user_details_not_auth(self):
        responce = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(responce, "username")
        keys = ["firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce, keys)

    @allure.title("Получение данных пользователя: авторизованный запрос, позитивный тест")
    @allure.description("Авторизованный запрос на данные того пользователя, под которым мы авторизованы. ОР: в ответе все поля")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(responce1, "user_id")

        responce2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(responce2, expected_fields)

    @allure.title("Получение данных пользователя: авторизованный запрос, негативный тест")
    @allure.description("Авторизуемся одним пользователем, пытаемся получить данные другого. ОР: в ответе только 'username'")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(responce1, "auth_sid")
        token = self.get_header(responce1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(responce1, "user_id")

        # Проверим, авторизованы ли мы?
        responce2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(responce2, expected_fields)

        # Возьмем другого пользователя:
        responce3 = MyRequests.get(f"/user/1")

        # Сделаем три проверки:
        # 1 - на наличие поля "username",
        # 2 - на то, что возвращается определенное значение в этом поле,
        # 3 - на то, что остальные поля, которые возвращаются только авторизованному пользователю, нам не вернулись.

        Assertions.assert_json_has_key(responce3, "username")
        u_name = self.get_json_value(responce3, "username")
        Assertions.assert_json_value_by_name(responce3, "username", u_name, f"This {u_name} doesn't exist")

        not_expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(responce3, not_expected_fields)
