from flask import Flask
from flasgger import Swagger

from core.config import settings

from cli.create_admin import create_admin
from admin.views import admin_bp
from api.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.app.secret_key
    app.config["DEBUG"] = settings.app.debug

    Swagger(app)

    # CLI commands
    app.cli.add_command(create_admin)

    # routes
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=settings.app.debug)
