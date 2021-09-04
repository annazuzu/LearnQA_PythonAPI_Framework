from requests import Response
import json


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value=None, error_message=None):
        if expected_value is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: {name}", f"Unexpected responce content {response.content}"
            return
        elif name == "email":
            assert response.content.decode(
                "utf-8") == "Invalid email format", f"Unexpected response content {response.content}"
        else:
            try:
                responce_as_dict = response.json()
            except json.decoder.JSONDecodeError:
                assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

            assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

            assert responce_as_dict[name] == expected_value, error_message

            if expected_value is None:
                assert response.content.decode(
                    "utf-8") == f"The following required params are missed: {name}", f"Unexpected responce content {response.content}"

    # Переделаем эту проверку под негативный тест:
    @staticmethod
    def assert_json_value_by_name_negative(response: Response, name, expected_value, error_message):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

        assert responce_as_dict[name] != expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        for name in names:
            assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert name not in responce_as_dict, f"Responce JSON shouldn't have key '{name}', but it's present"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        for name in names:
            assert name not in responce_as_dict, f"Responce JSON shouldn't have key '{name}', but it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_user_not_exist(response: Response, error_message):
        assert response.text == "User not found", f"Responce is JSON format. Responce text is '{response.text}'"

    @staticmethod
    def assert_user_is_exist(response: Response, error_message):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert "username" in responce_as_dict, f"Responce JSON doesn't have 'username'"

    @staticmethod
    def assert_too_long_or_short_name(response: Response, name, name_value, error_message):
        n = len(name_value)
        if 1 < n <= 250:
            return
        else:
            if n == 1:
                assert response.text == f"The value of '{name}' field is too short", f"Responce is JSON format. Responce text is '{response.text}'"
            elif n > 250:
                assert response.text == f"The value of '{name}' field is too long", f"Responce is JSON format. Responce text is '{response.text}'"
