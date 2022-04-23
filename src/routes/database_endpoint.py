from flask import Blueprint, current_app, request, jsonify
from models.ssh_handler import SSH
from models.log import Log
from models.file import File
import datetime

# Declare Blueprint
database_endpoint = Blueprint("database_endpoint", __name__)

# Route default path
ENDPOINT = "/databases"


@database_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    # Load configurations
    config = current_app.config['APP_CONFIG']
    cmds = current_app.config['APP_CMDS']

    try :
        # SSH handler
        handler = SSH(config.get('NAS_HOST'), config.get('NAS_USER'), config.get('NAS_PASS'))
        # Log database listingpxy  routine start on nasticot domaine
        Log(config.get('API_LOG'), 1, "backup routine", "List database backups", request.method, "backup").log()
        # SSH connection
        handler.connect()
        current_app.logger.debug("Retrieve existing databases backups")
        try:
            # Move to the right folder and display content
            output = handler.send(cmds.get("GET_DATABASES_MOVE"))
            # List for storing result
            result = []
            for line in iter(output.readline, ""):
                # Remove \n and split string
                rawArray = list(filter(None, line.rstrip("\n").split(" ")))
                # Build a list of File object
                result.append(File(name=rawArray[len(rawArray) - 1], size=rawArray[4], date=[rawArray[5], rawArray[6]]))
            
            return jsonify(files=[e.serialize() for e in result])

        except Exception as e:
            current_app.logger.error(e)

    except Exception as e:
        current_app.logger.error(f"An error occured while reaching endpoint {ENDPOINT}/backup : {e}")
    finally:
        handler.close()


@database_endpoint.route(f"{ENDPOINT}/backup", methods=["POST"])
def backup():

    # Retrieve post parameters
    databases = request.get_json(force=True)['databases']
 
    # Load configurations
    config = current_app.config['APP_CONFIG']
    cmds = current_app.config['APP_CMDS']

    try:
        # SSH handler
        handler = SSH(config.get('BESPIN_HOST'), config.get('PI_USER'), config.get('PI_PASS'))
        # Log database backup routine start on nasticot domaine
        Log(config.get('API_LOG'), 1, "backup routine", "backup databases", request.method, "backup").log()
        # SSH connection
        handler.connect()
        # Build dump cmd
        now = datetime.now()
        for db in databases: 
            current_app.logger.debug(f"Backup of database {db} started")
            file = f"{config.get['PI_SRC']}/{now.strftime('%d%m%Y')}_{db}.sql.gz"
            dump = f"mysqldump -u {config['MYSQL_USER']} -p{config['MYSQL_PASS']} {db} | gzip -c > {file};"
            copy = f"sshpass -p '{config['NAS_PASS']}' scp {file} ${config['NAS_USER']}@{config['NAS_HOST']}:{config['NAS_DEST']}/database"
            try:
                # Dumb dbs
                handler.send(dump)
                # Wait 3 sec
                time.sleep(3)
                # Move file to Synology
                handler.send(copy)
            except Exception as e:
                current_app.logger.error(e)
                continue

    except Exception as e:
        current_app.logger.error(f"An error occured while reaching endpoint {ENDPOINT}/backup : {e}")
        return e
    finally:
        handler.close()

    return ""
