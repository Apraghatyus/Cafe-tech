import os
from flask import Flask
from config import Config
from utils.db import db
from utils.jwt import init_jwt
from controllers.product_controller import product_bp
from controllers.pedido_controller import pedido_bp
from controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    init_jwt(app)

    app.register_blueprint(product_bp, url_prefix='/api/v1')
    app.register_blueprint(pedido_bp,  url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')

    return app

# Create the app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])