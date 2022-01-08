from flask import Blueprint, current_app

# Declare Blueprint
website_endpoint = Blueprint("website_endpoint", __name__)

# Route default path
ENDPOINT = "/sites"


@website_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    current_app.logger.debug("Retrieve existing databases")
    pass
