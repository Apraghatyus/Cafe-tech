from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from utils.api_response import ApiResponse
from schemas.auth_schema import LoginSchema
from services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)
login_schema = LoginSchema()
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    raw = request.get_json()
    if not isinstance(raw, dict):
        return ApiResponse.bad_request(message='JSON inválido o mal formado')

    try:
        creds = login_schema.load(raw)
    except ValidationError as err:
        return ApiResponse.bad_request(message=err.messages)

    user = auth_service.authenticate(creds['username'], creds['password'])
    if not user:
        return ApiResponse.bad_request(message='Credenciales inválidas')

    # Incluir el rol como claim adicional
    additional_claims = {'role': user.role}
    access_token = create_access_token(identity=user.username, additional_claims=additional_claims)

    return ApiResponse.ok(data=[{
        'access_token': access_token,
        'role': user.role
    }])
