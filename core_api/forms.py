from marshmallow.validate import Length
from marshmallow import Schema, fields


class CreateNewShortUrlForm(Schema):
    url = fields.Url(required=True)
    short_url = fields.String(required=False,
                              default=None,
                              validate=Length(max=8, min=4, error="Short URL will be at least 4 chars and max 8 chars"))
