import os
from datetime import datetime
from flask import Blueprint, current_app, request
from models.ssh_handler import SSH
from models.log import Log


# Declare Blueprint
database_endpoint = Blueprint("database_endpoint", __name__)

# Route default path
ENDPOINT = "/databases"


@database_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    current_app.logger.debug("Retrieve existing databases")
    return str(os.path.expanduser("~"))


@database_endpoint.route(f"{ENDPOINT}/backup", methods=["POST"])
def backup():

    # Retrieve post parameters
    databases = request.get_json(force=True)['databases']
    
    # Load configurations
    SSH_HOST = os.environ.get("BESPIN_HOST")
    SSH_USER = os.environ.get("BESPIN_USER")
    SSH_PASS = os.environ.get("BESPIN_PASS")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASS = os.environ.get("MYSQL_PASS")
    API_LOG = os.environ.get("API_LOG")
    
    try:
        # Log database backup routine start on nasticot domaine
        Log(API_LOG, 1, "backup routine", "backup databases", request.method, "backup").log()
        # SSH connection
        handler = SSH(SSH_HOST, SSH_USER, SSH_PASS)
        handler.connect()
        # Build dump cmd
        now = datetime.now()
        for db in databases:
            current_app.logger.debug(f"Backup of database {db} started")
            dt_string = now.strftime("%d%m%Y-%H:%M:%S")
            filename = dt_string + f"_{db}_auto.sql.gz"
            cmd = f"mysqldump -u {MYSQL_USER} -p{MYSQL_PASS} {db} | gzip -c > {filename};"
            # Send command
            handler.send(cmd)

    except Exception as e:
        print(e)
    finally:
        handler.close()

    return ""
