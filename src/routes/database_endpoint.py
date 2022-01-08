import os, time
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
    config = current_app.config['APP_CONFIG']

    try:
        # SSH handler
        handler = SSH(config['SSH_HOST'], config['SSH_USER'], config['SSH_PASS'])
        # Log database backup routine start on nasticot domaine
        #Log(config['API_LOG'], 1, "backup routine", "backup databases", request.method, "backup").log()
        # SSH connection
        handler.connect()
        # Build dump cmd
        now = datetime.now()
        for db in databases: 
            current_app.logger.debug(f"Backup of database {db} started")
            filename = now.strftime("%d%m%Y") + f"_{db}.sql.gz"
            dump = f"mysqldump -u {config['MYSQL_USER']} -p{config['MYSQL_PASS']} {db} | gzip -c > {filename};"
            copy = f"sshpass -p 'Yanover225712' scp /home/nasticot/{filename} yanover@192.168.0.10:/volume1/Partage/BackUp/Nasticot/database"
            try:
                # Dumb dbs
                handler.send(dump)
                # Wait 
                time.sleep(3)
                # Move file to Synology
                handler.send(copy)
            except Exception as e:
                current_app.logger.debug(e)
                continue

    except Exception as e:
        current_app.logger.debug(f"An error occured while reaching endpoint {ENDPOINT}/backup : {e}")
        return e
    finally:
        handler.close()

    return ""
