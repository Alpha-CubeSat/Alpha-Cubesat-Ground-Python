from flask import Flask, request
from markupsafe import escape

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from api.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')
    from api.rockblock import rockblock
    app.register_blueprint(rockblock, url_prefix='/api/rockblock')
    from api.cubesat import cubesat
    app.register_blueprint(cubesat, url_prefix='/api/cubesat')
    from api.errors import errors
    app.register_blueprint(errors)

    @app.get('/api/debug/ping')
    def ping(): return 'pong'

    @app.post('/api/debug/echo')
    def echo(): return escape(request.data)

    return app