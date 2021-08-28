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
        assert responce_as_dict[name] == expected_value, error_message

