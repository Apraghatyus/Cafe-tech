from typing import Dict, Any, Optional, Tuple, List
from repositories.pedido_repository import PedidoRepository
from models.pedido import Pedido

class PedidoService:
    def __init__(self):
        self.pedido_repository = PedidoRepository()

    def list(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Lista pedidos paginados"""
        items, total = self.pedido_repository.list_paginated(page, per_page)
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

    def get(self, id: int) -> Optional[Pedido]:
        """Obtiene un pedido por ID"""
        return self.pedido_repository.get_by_id(id)

    def create(self, data: Dict[str, Any]) -> Pedido:
        """Crea un nuevo pedido"""
        if not isinstance(data, dict):
            raise ValueError("Los datos deben ser un diccionario")
        
        # Validar campos requeridos
        required_fields = ['cliente', 'producto_id', 'cantidad', 'fecha_entrega', 'estado']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        return self.pedido_repository.create(data)

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Pedido]:
        """Actualiza un pedido existente"""
        if not isinstance(data, dict):
            raise ValueError("Los datos deben ser un diccionario")
        
        return self.pedido_repository.update(id, data)

    def delete(self, id: int) -> Optional[Pedido]:
        """Elimina un pedido"""
        return self.pedido_repository.delete(id)