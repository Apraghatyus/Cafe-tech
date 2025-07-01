import os
from datetime import timedelta

class Config:
    # URL de la base de datos (heredada de la env var o fallback)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://root:toor@db:5432/technicial_test'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambia-esta-clave')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'otra-clave-secreta')
    # Tiempo de expiración del token de acceso (por defecto 1 hora)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
