from marshmallow.validate import Length, ValidationError
from marshmallow import Schema, fields, pre_load, post_load
from hashlib import md5


class CreateNewShortUrlForm(Schema):
    url = fields.Url(required=True)
    short_url = fields.String(required=False,
                              default=None,
                              validate=Length(max=8,
                                              min=4,
                                              error="Short URL should be at least 4 chars and max 8 chars"))


class UserRegistrationForm(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True,
                             validate=Length(max=20,
                                             min=6,
                                             error="Password should be at least 6 chars and max 20 chars"))
    confirm_password = fields.String(required=True)

    @pre_load
    def check_confirm_password(self, data):
        if data.get("password") and data.get("confirm_password"):
            if data["password"] == data["confirm_password"]:
                return data
            else:
                raise ValidationError("password and confirm_password should be equal.",
                                      field_names=["password", "confirm_password"])

    @post_load
    def password_hash(self, data):
        data.pop("confirm_password")
        password = md5(data["password"].encode())
        data["password"] = password.hexdigest()
        return data


class UserAuthForm(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def password_hash(self, data):
        password = md5(data["password"].encode())
        data["password"] = password.hexdigest()
        return data
