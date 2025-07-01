from flask_jwt_extended import JWTManager

jwt = JWTManager()

def init_jwt(app):
    """
    Inicializa Flask-JWT-Extended en la app Flask.
    """
    jwt.init_app(app)

    # Opcional: personalizar respuestas de error JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token expirado'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return {'error': 'Token inválido'}, 422

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return {'error': 'Token faltante'}, 401
