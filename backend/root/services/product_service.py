from typing import Dict, Any, Optional, List
from repositories.product_repository import ProductRepository
from models.product import Product

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def list(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Lista productos paginados"""
        items, total = self.product_repository.list_paginated(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        return {
            "items": items,
            "pagination": {
                "page": page,
                "per_page": min(per_page, 10),
                "total": total,
                "total_pages": total_pages
            }
        }

    def get(self, id: int) -> Optional[Product]:
        """Obtiene un producto por ID"""
        return self.product_repository.get_by_id(id)

    def create(self, data: Dict[str, Any]) -> Product:
        """Crea un nuevo producto"""
        if not isinstance(data, dict):
            raise ValueError("Los datos deben ser un diccionario")
        
        # Validar campos requeridos
        required_fields = ['nombre', 'precio']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        return self.product_repository.create(data)

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Product]:
        """Actualiza un producto existente"""
        if not isinstance(data, dict):
            raise ValueError("Los datos deben ser un diccionario")
        
        return self.product_repository.update(id, data)

    def delete(self, id: int) -> Optional[Product]:
        """Elimina un producto"""
        return self.product_repository.delete(id)