from typing import Tuple, List, Optional, Dict, Any
from utils.db import db
from models.pedido import Pedido
from sqlalchemy.exc import SQLAlchemyError

class PedidoRepository:
    def list_paginated(self, page: int, per_page: int = 10) -> Tuple[List[Pedido], int]:
        """Lista pedidos paginados"""
        try:
            per_page = min(per_page, 10)
            query = Pedido.query.order_by(Pedido.id)
            items = query.limit(per_page).offset((page-1)*per_page).all()
            total = query.count()
            return items, total
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al listar pedidos: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Pedido]:
        """Obtiene un pedido por ID"""
        try:
            return Pedido.query.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al obtener pedido: {str(e)}")

    def create(self, data: Dict[str, Any]) -> Pedido:
        """Crea un nuevo pedido"""
        try:
            # Crear instancia del pedido con validación de tipos
            ped = Pedido(
                cliente=str(data['cliente']),
                producto_id=int(data['producto_id']),
                cantidad=int(data['cantidad']),
                fecha_entrega=data['fecha_entrega'],  # Marshmallow ya lo convierte a date
                estado=str(data['estado'])
            )
            
            db.session.add(ped)
            db.session.commit()
            return ped
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear pedido: {str(e)}")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            raise Exception(f"Datos inválidos: {str(e)}")

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Pedido]:
        """Actualiza un pedido existente"""
        try:
            ped = self.get_by_id(id)
            if not ped:
                return None
            
            # Actualizar solo los campos proporcionados
            for key, val in data.items():
                if hasattr(ped, key):
                    # Validación de tipos básica
                    if key in ['cliente', 'estado']:
                        val = str(val)
                    elif key in ['producto_id', 'cantidad']:
                        val = int(val)
                    
                    setattr(ped, key, val)
            
            db.session.commit()
            return ped
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar pedido: {str(e)}")
        except (ValueError, TypeError) as e:
            db.session.rollback()
            raise Exception(f"Datos inválidos: {str(e)}")

    def delete(self, id: int) -> Optional[Pedido]:
        """Elimina un pedido"""
        try:
            ped = self.get_by_id(id)
            if not ped:
                return None
            
            db.session.delete(ped)
            db.session.commit()
            return ped
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar pedido: {str(e)}")