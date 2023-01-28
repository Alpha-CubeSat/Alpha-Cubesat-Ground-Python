from apifairy import APIFairy
from flask import Flask, redirect, url_for
from flask_marshmallow import Marshmallow

from config import Config

ma = Marshmallow()
apifairy = APIFairy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ma.init_app(app)
    apifairy.init_app(app)

    from api.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')
    from api.rockblock import rockblock
    app.register_blueprint(rockblock, url_prefix='/api/rockblock')
    from api.cubesat import cubesat
    app.register_blueprint(cubesat, url_prefix='/api/cubesat')
    from api.errors import errors
    app.register_blueprint(errors)
    from api.debug import debug
    app.register_blueprint(debug, url_prefix='/api/debug')

    from api import users_db
    users_db.init_app(app)

    @app.route('/')
    @app.route('/api')
    def index():
        return redirect(url_for('apifairy.docs'))

    return app