from marshmallow import Schema, fields, validate, post_load, ValidationError
from decimal import Decimal, InvalidOperation
from typing import Dict, Any

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'El campo nombre es obligatorio'}
    )
    precio = fields.Decimal(
        required=True,
        as_string=False,  # Cambiado para mejor manejo de tipos
        validate=validate.Range(min=0),
        error_messages={'required': 'El campo precio es obligatorio'}
    )
    descripcion = fields.Str(
        allow_none=True,
        missing=None,  # Valor por defecto si no se proporciona
        validate=validate.Length(max=500)  # Límite de longitud
    )

    @post_load
    def make_dict(self, data, **kwargs) -> Dict[str, Any]:
        """
        Asegura que el resultado del load() siempre sea un diccionario
        con los tipos correctos
        """
        # Validación del precio
        if 'precio' in data:
            try:
                # Convertir a Decimal si es string o float
                if isinstance(data['precio'], str):
                    data['precio'] = Decimal(data['precio'])
                elif isinstance(data['precio'], (int, float)):
                    data['precio'] = Decimal(str(data['precio']))
                elif not isinstance(data['precio'], Decimal):
                    raise ValidationError('El precio debe ser un número válido')
                
                # Validar que sea positivo
                if data['precio'] < 0:
                    raise ValidationError('El precio no puede ser negativo')
                
                # Validar que tenga máximo 2 decimales para precios
                if data['precio'].as_tuple().exponent < -2:
                    raise ValidationError('El precio no puede tener más de 2 decimales')
                    
            except (InvalidOperation, ValueError):
                raise ValidationError('El precio debe ser un número válido')
        
        # Asegurar tipos correctos
        result: Dict[str, Any] = {}
        for key, value in data.items():
            if key == 'nombre':
                result[key] = str(value).strip()
            elif key == 'precio':
                result[key] = value  # Ya es Decimal por la validación anterior
            elif key == 'descripcion':
                result[key] = str(value).strip() if value is not None else None
            else:
                result[key] = value
        
        return result


# Funciones helper para usar en el controlador
def validate_and_load_product(schema: ProductSchema, data: Dict[str, Any], partial: bool = False) -> Dict[str, Any]:
    """
    Función helper para validar y cargar datos de producto
    Garantiza tipo de retorno correcto
    """
    try:
        if partial:
            result = schema.load(data, partial=True)
        else:
            result = schema.load(data)
        
        # Double check que es dict
        if not isinstance(result, dict):
            raise ValidationError("Tipo de datos inválido después de la validación")
        
        return result
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Error en validación: {str(e)}")