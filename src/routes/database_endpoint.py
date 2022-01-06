import os
from flask import Blueprint, current_app
from models.mysql_handler import MYSQL
from models.ssh_handler import SSH


# Declare Blueprint
database_endpoint = Blueprint("database_endpoint", __name__)

# Route default path
ENDPOINT = "/databases"


@database_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    current_app.logger.debug("Retrieve existing databases")
    return str(os.path.expanduser("~"))


@database_endpoint.route(f"{ENDPOINT}/backup", methods=["GET"])
def backup():
    # Log database backup routine start on nasticot domaine
    # --> here
    # Load configurations
    HOST = os.environ.get("BESPIN_HOST")
    USER = os.environ.get("BESPIN_USER")
    PASS = os.environ.get("BESPIN_PASS")
    # SSH connection to host
    handler = SSH(HOST, USER, PASS)
    handler.connect()
    handler.send("pwd")
    
    


    return ""
