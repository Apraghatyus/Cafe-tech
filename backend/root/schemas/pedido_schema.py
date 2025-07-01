from marshmallow import Schema, fields, validate, ValidationError
from typing import Dict, Any

class PedidoSchema(Schema):
    """Schema simplificado para evitar problemas de tipos"""
    
    id = fields.Int(dump_only=True)
    cliente = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        allow_none=False,
        error_messages={'required': 'El campo cliente es obligatorio'}
    )
    producto_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        allow_none=False,
        error_messages={'required': 'El campo producto_id es obligatorio'}
    )
    cantidad = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        allow_none=False,
        error_messages={'required': 'El campo cantidad es obligatorio'}
    )
    fecha_entrega = fields.Date(
        required=True,
        allow_none=False,
        error_messages={'required': 'El campo fecha_entrega es obligatorio'}
    )
    estado = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        allow_none=False,
        error_messages={'required': 'El campo estado es obligatorio'}
    )

    def load_pedido_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método helper para cargar y validar datos específicamente
        Garantiza que siempre retorne Dict[str, Any]
        """
        try:
            # Usar el load estándar de marshmallow
            result = self.load(json_data)
            
            # Asegurar que el resultado es un diccionario
            if not isinstance(result, dict):
                raise ValidationError("Error interno: resultado de deserialización inválido")
            
            # Validación adicional de tipos
            validated_data: Dict[str, Any] = {}
            
            for key, value in result.items():
                if key == 'cliente':
                    validated_data[key] = str(value).strip()
                elif key == 'estado':
                    validated_data[key] = str(value).strip()
                elif key == 'producto_id':
                    validated_data[key] = int(value)
                elif key == 'cantidad':
                    validated_data[key] = int(value)
                elif key == 'fecha_entrega':
                    # Marshmallow ya convierte a date object
                    validated_data[key] = value
                else:
                    validated_data[key] = value
            
            return validated_data
            
        except ValidationError:
            raise  # Re-raise ValidationError as is
        except Exception as e:
            raise ValidationError(f"Error de validación: {str(e)}")

# Funciones helper para usar en el controlador
def validate_and_load_pedido(schema: PedidoSchema, data: Dict[str, Any], partial: bool = False) -> Dict[str, Any]:
    """
    Función helper para validar y cargar datos de pedido
    Garantiza tipo de retorno correcto
    """
    try:
        if partial:
            result = schema.load(data, partial=True)
        else:
            result = schema.load_pedido_data(data)
        
        # Double check que es dict
        if not isinstance(result, dict):
            raise ValidationError("Tipo de datos inválido después de la validación")
        
        return result
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Error en validación: {str(e)}")