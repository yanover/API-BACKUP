from flask import Blueprint, current_app, request

# Declare Blueprint
container_endpoint = Blueprint("container_endpoint", __name__)

# Route default path
ENDPOINT = "/containers"


@container_endpoint.route(ENDPOINT, methods=["POST"])
def default():
     # Retrieve post parameters
    sites = request.get_json(force=True)['sites']
    print(sites)
    return ""
