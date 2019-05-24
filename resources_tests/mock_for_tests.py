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