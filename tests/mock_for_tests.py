from .fixtures import ALL_URLS_DATA

TEST_USER_URL = ALL_URLS_DATA[2]

URL_POST_DATA = {"url": "https://docs.djangoproject.com/en/2.1/ref/models/querysets/"}

URL_POST_DATA_WITH_VALID_SHORT_URL = {"url": "https://docs.djangoproject.com/en/2.1/ref/models/querysets/",
                                      "short_url": "hfht4d"}

URL_POST_DATA_WITH_INVALID_SHORT_URL = {"url": "https://docs.djangoproject.com/en/2.1/ref/models/querysets/",
                                        "short_url": "hfht4dhjutyujtutyuytuytyutuytuty"}
URL_VALIDATION_ERROR = {
    "url": [
        "Missing data for required field."
    ]
}

SHORT_URL_VALIDATION_ERROR = {
    "short_url": [
        "Short URL should be at least 4 chars and max 8 chars"
    ]
}

ANOTHER_USER_URL = ALL_URLS_DATA[0]

NOT_FOUND_URL_ERROR = {
    "error": "This url not found for this user"
}

USER_REGISTRATION_VALID_DATA = {"username": "test_new",
                                "password": "Test2019",
                                "confirm_password": "Test2019"}

USER_REGISTRATION_INVALID_PASSWORD_CONFIRMATION_DATA = {"username": "test_new",
                                                        "password": "Test2019",
                                                        "confirm_password": "Test000"}

USER_REGISTRATION_INVALID_PASSWORD_LENGTH_DATA = {"username": "test_new",
                                                  "password": "Test",
                                                  "confirm_password": "Test"}

USER_REGISTRATION_EXISTS_USERNAME_DATA = {"username": "test",
                                          "password": "Test2019",
                                          "confirm_password": "Test2019"}

PASSWORD_CONFIRMATION_ERROR = {
    "password": [
        "password and confirm_password should be equal."
    ],
    "confirm_password": [
        "password and confirm_password should be equal."
    ]
}

PASSWORD_LENGTH_ERROR = {
    "password": [
        "Password should be at least 6 chars and max 20 chars"
    ]
}

REGISTRATION_REQUIRED_FIELDS_ERROR = {
    "confirm_password": [
        "Missing data for required field."
    ],
    "username": [
        "Missing data for required field."
    ],
    "password": [
        "Missing data for required field."
    ]
}

USERNAME_EXISTS_ERROR = {"error": "User with this username already exists"}

EMPTY_POST_REQUEST_ERROR = "Error: POST request data should not be None"


AUTH_USER_CORRECT_DATA = {"username": "test",
                          "password": "Test2018"}


AUTH_USER_REQUIRED_FIELDS_ERROR = {
    "password": [
        "Missing data for required field."
    ],
    "username": [
        "Missing data for required field."
    ]
}
