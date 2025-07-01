from flask import Blueprint, request
from typing import Any, Dict, cast
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from services.product_service import ProductService
from schemas.product_schema import ProductSchema
from utils.api_response import ApiResponse

product_bp    = Blueprint('product_bp', __name__)
schema_many   = ProductSchema(many=True)
schema_single = ProductSchema()
service       = ProductService()

@product_bp.route('/products', methods=['GET'])
#@jwt_required()
def get_products():
    try:
        page     = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        return ApiResponse.bad_request(message="Los parámetros page y per_page deben ser enteros")

    result = service.list(page, per_page)
    data   = schema_many.dump(result["items"])
    return ApiResponse.ok(
        data=data,
        total=result["pagination"]["total"],
        pagination=result["pagination"]
    )

@product_bp.route('/product/<int:id>', methods=['GET'])
#@jwt_required()
def get_product(id: int):
    prod = service.get(id)
    if not prod:
        return ApiResponse.not_found("Producto", resource_id=id)
    return ApiResponse.ok(data=schema_single.dump(prod))

@product_bp.route('/product', methods=['POST'])
#@jwt_required()
def create_product():
    # Validación del JSON recibido
    try:
        raw = request.get_json()
        if raw is None:
            return ApiResponse.bad_request(message="No se proporcionó JSON válido")
        if not isinstance(raw, dict):
            return ApiResponse.bad_request(message="El JSON debe ser un objeto")
    except Exception:
        return ApiResponse.bad_request(message="JSON inválido o mal formado")

    # Validación y deserialización con Marshmallow
    try:
        # El post_load del schema garantiza que esto será Dict[str, Any]
        loaded_data = schema_single.load(raw)
        payload: Dict[str, Any] = cast(Dict[str, Any], loaded_data)
        
    except ValidationError as err:
        return ApiResponse.bad_request(message="Errores de validación")
    except Exception as err:
        return ApiResponse.bad_request(message=f"Error al procesar datos: {str(err)}")

    # Crear el producto
    try:
        prod = service.create(payload)
        return ApiResponse.created(data=schema_single.dump(prod))
    except Exception as err:
        return ApiResponse.bad_request(message=f"Error al crear producto: {str(err)}")

@product_bp.route('/product/<int:id>', methods=['PUT'])
#@jwt_required()
def update_product(id: int):
    # Validación del JSON recibido
    try:
        raw = request.get_json()
        if raw is None:
            return ApiResponse.bad_request(message="No se proporcionó JSON válido")
        if not isinstance(raw, dict):
            return ApiResponse.bad_request(message="El JSON debe ser un objeto")
    except Exception:
        return ApiResponse.bad_request(message="JSON inválido o mal formado")

    # Validación y deserialización con Marshmallow
    try:
        # Para updates, usamos partial=True para permitir actualizaciones parciales
        loaded_data = schema_single.load(raw, partial=True)
        payload: Dict[str, Any] = cast(Dict[str, Any], loaded_data)
        
    except ValidationError as err:
        return ApiResponse.bad_request(message="Errores de validación")
    except Exception as err:
        return ApiResponse.bad_request(message=f"Error al procesar datos: {str(err)}")

    # Actualizar el producto
    try:
        prod = service.update(id, payload)
        if not prod:\
            return ApiResponse.not_found("Producto", resource_id=id)
        return ApiResponse.updated(data=schema_single.dump(prod))
    except Exception as err:
        return ApiResponse.bad_request(message=f"Error al actualizar producto: {str(err)}")

@product_bp.route('/product/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_product(id: int):
    try:
        prod = service.delete(id)
        if not prod:
            return ApiResponse.not_found("Producto", resource_id=id)
        return ApiResponse.deleted(deleted_id=id)
    except Exception as err:
        return ApiResponse.bad_request(message=f"Error al eliminar producto: {str(err)}")