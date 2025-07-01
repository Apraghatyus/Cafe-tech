from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """Esquema para validar credenciales de login."""

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={'required': 'El campo username es obligatorio'}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, max=128),
        error_messages={'required': 'El campo password es obligatorio'}
    )

class AuthSchema(Schema):
    """Esquema para serializar/deserializar la entidad Auth (usuarios)."""

    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={'required': 'El campo username es obligatorio'}
    )
    password = fields.Str(
        load_only=True,
        validate=validate.Length(min=6, max=128)
    )
    role = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=10),
        error_messages={'required': 'El campo role es obligatorio'}
    )