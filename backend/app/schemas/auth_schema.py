from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
