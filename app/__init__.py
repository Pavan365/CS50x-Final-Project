# Import standard libraries.
import os

# Import external libraries.
from flask import Flask
from flask_session import Session

# Import local modules.
from . import authenticate
from . import database
from . import options


def create_app():
    """ Creates and configures the app. """

    # Create the app.
    app = Flask(__name__, instance_relative_config=True)

    # Configure the app.
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "app.db"),
                            SESSION_PERMENANT=False, SESSION_TYPE="filesystem")
    app.after_request(disable_caching)

    # Configure the session, database and blueprints.
    Session(app)
    database.init_app(app)
    app.register_blueprint(authenticate.bp)
    app.register_blueprint(options.bp)

    return app


def disable_caching(response):
    """ Disables caching of responses. """

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
