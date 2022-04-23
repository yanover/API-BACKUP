from flask import Blueprint, current_app, request, jsonify
from models.ssh_handler import SSH
from models.log import Log
from models.file import File
from datetime import datetime

# Declare Blueprint
container_endpoint = Blueprint("container_endpoint", __name__)

# Route default path
ENDPOINT = "/containers"

@container_endpoint.route(ENDPOINT, methods=["GET"])
def default():
    # Load configurations
    config = current_app.config['APP_CONFIG']

    try :
        # SSH handler
        handler = SSH(config['NAS_HOST'], config['NAS_USER'], config['NAS_PASS'])
        # Log database listingpxy  routine start on nasticot domaine
        Log(config['API_LOG'], 1, "backup routine", "List containers backups", request.method, "backup").log()
        # SSH connection
        handler.connect()
        current_app.logger.debug("Retrieve existing containers backups")
        try:
            # Move to the right folder and display content
            output = handler.send(f"cd {config['NAS_DEST']}/containers;ls -alh --fu | grep '^-'")
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


@container_endpoint.route(f"{ENDPOINT}/backup", methods=["POST"])
def backup():

    # Retrieve post parameters
    hosts = request.get_json(force=True)['hosts']
    
    # Load configurations
    config = current_app.config['APP_CONFIG']

    # Build command to save containers

    try:
        for host in hosts:

            # SSH handler
            handler = SSH(host, config['PI_USER'], config['PI_PASS'])
            
            # Log database backup routine start on nasticot domaine
            Log(config['API_LOG'], 1, "backup routine", "backup databases", request.method, "backup").log()
            
            # SSH connection
            handler.connect()
            # Build dump cmd
            now = datetime.now()           
            # Get containers on current host
            containers = []
            output = handler.send("/snap/bin/lxc ls -c n --format csv")

            for line in iter(output.readline, ""):
                # Remove \n and split string
                containers.extend(list(filter(None, line.rstrip("\n").split(" ")))) 

            for container in containers:
                # Save containers
                current_app.logger.debug(f"Backup of container {container} started")
                file = f"{config['PI_SRC']}/{now.strftime('%d%m%Y')}_{container}.tar.xz"
                dump = f"""/snap/bin/lxc export {container} {file} --optimized-storage"""  
                copy = f"sshpass -p '{config['NAS_PASS']}' scp {file} ${config['NAS_USER']}@{config['NAS_HOST']}:{config['NAS_DEST']}/database"
                try :
                    print(f"saving container : {container}")
                    print(f"Sending command {dump}")
                    print(f"Sending command {copy}")
                    # Dump container
                    # handler.send(dump)                                
                    # Move container
                    # handler.send(copy)
                except:
                    current_app.logger.debug(f"An error occured while saving container {container}, swapping to next one")
                    continue

    except Exception as e:
        current_app.logger.error(f"An error occured while reaching endpoint {ENDPOINT}/backup : {e}")
        return e
    finally:
        handler.close()

    return ""
