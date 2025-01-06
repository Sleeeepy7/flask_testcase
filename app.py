from flask import Flask

from core.config import settings

from cli.create_admin import create_admin


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.app.secret_key
    app.config["DEBUG"] = settings.app.debug

    app.cli.add_command(create_admin)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=settings.app.debug)
