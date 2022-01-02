import os
from flask import Blueprint, request, abort, current_app
from models.mysql_handler import MYSQL
from MySQLdb import _mysql

# Declare Blueprint
database_endpoint = Blueprint("database_endpoint", __name__)

# Route default path
ENDPOINT = "/mysql"

@database_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    current_app.logger.debug("Retrieve existing databases")
    pass


@database_endpoint.route(f"{ENDPOINT}/backup", methods=["GET"])
def backup():

    # Load configurations
    HOST = os.environ.get("MYSQL_HOST")
    PORT = int(os.environ.get("MYSQL_PORT"))
    USER = os.environ.get("MYSQL_USER")
    PASS = os.environ.get("MYSQL_PASS")

    database = MYSQL(HOST, PORT, USER, PASS)
    handler = database.connect()
    print(handler.query("SHOW DATABASES;"))
    return ""