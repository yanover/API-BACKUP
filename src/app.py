import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from logging.config import dictConfig
from routes.database_endpoint import database_endpoint
from routes.container_endpoint import container_endpoint
from common.errors.HttpExceptions import LogError, AuthException, SshException
from common.utils.constants import Constants

# Global
PORT = os.environ.get("PORT")
PREFIX = os.environ.get("PREFIX")
APP = Flask(__name__)
# Enable cors
CORS(APP)
cors = CORS(APP, resource={
    r"/*":{
        "origins":"*"
    }
})
# Load .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Default route
@APP.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'

# Default configuration
def setup(APP):
    # Load default configuration into context
    constants = Constants()
    APP.config["APP_CONFIG"] = constants.APP_CONFIG
    APP.config["APP_CMDS"] = constants.APP_CMDS

    # Configure logging
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )


def bad_request(e):
    return e, 400


def unauthorized(e):
    print(e)
    return e, 401


def not_found(e):
    return e, 404


# Load errors
def register_errors(app):
    app.logger.info("Registering error handlers ..")
    app.register_error_handler(LogError, bad_request)
    app.register_error_handler(SshException, bad_request)
    app.register_error_handler(AuthException, unauthorized)


# Load endpoints
def register_endpoints(app):
    app.logger.info("Registering endpoint ..")
    # Database
    app.register_blueprint(database_endpoint, url_prefix=PREFIX)
    # Containers
    app.register_blueprint(container_endpoint, url_prefix=PREFIX)


# Run webserver
def run(app):
    app.logger.info("Launching webserver ..")
    app.run(debug=True, port=PORT, host="0.0.0.0")


if __name__ == "__main__":
    # Set default configuration
    setup(APP)
    # Register errors
    register_errors(APP)
    # Register endpoints
    register_endpoints(APP)
    # Launch webserver
    run(APP)
