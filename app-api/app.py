"""
    comprenhensive imports
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from routes import register_routes

"""
    initialise the jwt manager
"""
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = '6007d3737a6d86232f11dfe130d2c0cd771bb8a6e23b7b52346a8abb26a1ff1d'
    jwt.init_app(app)
    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    