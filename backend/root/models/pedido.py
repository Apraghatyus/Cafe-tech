from utils.db import db
from typing import Optional
from datetime import date

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id: int = db.Column(db.Integer, primary_key=True)
    cliente: str = db.Column(db.String(100), nullable=False)
    producto_id: int = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad: int = db.Column(db.Integer, nullable=False)
    fecha_entrega: date = db.Column(db.Date, nullable=False)
    estado: str = db.Column(db.String(50), nullable=False)

    # Asegúrate de que el nombre de la clase coincida con tu modelo Product
    # Si tu modelo se llama 'Product', úsalo; si es 'Producto', cámbialo
    producto = db.relationship('Product', backref='pedidos')
    
    def __init__(self, cliente: str, producto_id: int, cantidad: int, fecha_entrega: date, estado: str):
        self.cliente = cliente
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha_entrega = fecha_entrega
        self.estado = estado
    
    def __repr__(self):
        return f'<Pedido {self.id}: {self.cliente}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para serialización"""
        return {
            'id': self.id,
            'cliente': self.cliente,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'fecha_entrega': self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            'estado': self.estado
        }