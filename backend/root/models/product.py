from utils.db import db
from typing import Optional
from decimal import Decimal

class Product(db.Model):
    __tablename__ = 'productos'

    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    precio: Decimal = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion: Optional[str] = db.Column(db.Text, nullable=True)

    # Relación inversa con pedidos (si la necesitas)
    # pedidos = db.relationship('Pedido', backref='producto', lazy=True)
    
    def __init__(self, nombre: str, precio: Decimal, descripcion: Optional[str] = None):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
    
    def __repr__(self):
        return f'<Product {self.id}: {self.nombre}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para serialización"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': float(self.precio) if self.precio else 0.0,
            'descripcion': self.descripcion
        }