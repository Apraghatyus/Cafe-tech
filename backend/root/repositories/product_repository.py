from typing import Tuple, List, Optional, Dict, Any
from decimal import Decimal
from utils.db import db
from models.product import Product
from sqlalchemy.exc import SQLAlchemyError

class ProductRepository:
    def list_paginated(self, page: int, per_page: int = 10) -> Tuple[List[Product], int]:
        """Lista productos paginados"""
        try:
            per_page = min(per_page, 10)
            query = Product.query.order_by(Product.id)
            items = query.limit(per_page).offset((page-1)*per_page).all()
            total = query.count()
            return items, total
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al listar productos: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Product]:
        """Obtiene un producto por ID"""
        try:
            return Product.query.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al obtener producto: {str(e)}")

    def create(self, data: Dict[str, Any]) -> Product:
        """Crea un nuevo producto"""
        try:
            # Crear instancia del producto con validación de tipos
            prod = Product(
                nombre=str(data['nombre']),
                precio=data['precio'],  # Ya es Decimal del schema
                descripcion=str(data['descripcion']) if data.get('descripcion') else None
            )
            
            db.session.add(prod)
            db.session.commit()
            return prod
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear producto: {str(e)}")
        except (ValueError, KeyError) as e:
            db.session.rollback()
            raise Exception(f"Datos inválidos: {str(e)}")

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Product]:
        """Actualiza un producto existente"""
        try:
            prod = self.get_by_id(id)
            if not prod:
                return None
            
            # Actualizar solo los campos proporcionados
            for key, val in data.items():
                if hasattr(prod, key):
                    # Validación de tipos básica
                    if key == 'nombre':
                        val = str(val)
                    elif key == 'precio':
                        # val ya es Decimal del schema
                        pass
                    elif key == 'descripcion':
                        val = str(val) if val is not None else None
                    
                    setattr(prod, key, val)
            
            db.session.commit()
            return prod
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar producto: {str(e)}")
        except (ValueError, TypeError) as e:
            db.session.rollback()
            raise Exception(f"Datos inválidos: {str(e)}")

    def delete(self, id: int) -> Optional[Product]:
        """Elimina un producto"""
        try:
            prod = self.get_by_id(id)
            if not prod:
                return None
            
            db.session.delete(prod)
            db.session.commit()
            return prod
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar producto: {str(e)}")