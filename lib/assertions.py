from requests import Response
import json


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            responce_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Responce is not JSON format. Responce text is '{response.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

        value = responce_as_dict[name]

        if value == "email":
            assert response.content.decode(
                "utf-8") == "Invalid email format", f"Unexpected response content {response.content}"
        elif len(value) > 250:
            assert response.content.decode(
                "utf-8") == f"The value of '{value}' field is too long", f"Unexpected response content {response.content}"
        elif len(value) < 10:
            assert response.content.decode(
                "utf-8") == f"The value of '{value}' field is too short", f"Unexpected response content {response.content}"

        assert value == expected_value, error_message



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
