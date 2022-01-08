import os
from flask import Flask
from werkzeug.exceptions import BadRequest, NotFound
from logging.config import dictConfig
from routes.database_endpoint import database_endpoint
from routes.website_endpoint import website_endpoint
from common.errors.LogError import LogError

# Global
PORT = os.environ.get("PORT")
PREFIX = os.environ.get("PREFIX")
APP = Flask(__name__)

# Default configuration
def setup(APP):
    # Load default configuration into context
    APP.config['APP_CONFIG'] = {
        'SSH_HOST' : os.environ.get("BESPIN_HOST"),
        'SSH_USER' : os.environ.get("BESPIN_USER"),
        'SSH_PASS' : os.environ.get("BESPIN_PASS"),
        'MYSQL_USER' : os.environ.get("MYSQL_USER"),
        'MYSQL_PASS' : os.environ.get("MYSQL_PASS"),
        'API_LOG' : os.environ.get("API_LOG")
    }
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

def not_found(e):
    return e, 404

# Load errors
def register_errors(app):
    app.register_error_handler(LogError, bad_request)

# Load endpoints
def register_endpoints(app):
    app.logger.info("Loading endpoint ..")
    # Database
    app.register_blueprint(database_endpoint, url_prefix=PREFIX)
    # Website
    app.register_blueprint(website_endpoint, url_prefix=PREFIX)


# Run webserver
def run(app):
    app.logger.info("Launching webserver ..")
    app.run(debug=True, port=PORT)


if __name__ == "__main__":
    # Set default configuration
    setup(APP)
    # Register errors
    register_errors(APP)
    # Register endpoints
    register_endpoints(APP)
    # Launch webserver
    run(APP)
