from flask import Blueprint, current_app, request
from models.ssh_handler import SSH

# Declare Blueprint
container_endpoint = Blueprint("container_endpoint", __name__)

# Route default path
ENDPOINT = "/containers"


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
            
            # Get containers on current host
            containers = []
            output = handler.send("/snap/bin/lxc ls -c n --format csv")

            for line in iter(output.readline, ""):
                # Remove \n and split string
                containers.extend(list(filter(None, line.rstrip("\n").split(" ")))) 

            for container in containers:
                # Save containers
                current_app.logger.debug(f"Backup of container {container} started")
                try :
                    handler.send(f"""/snap/bin/lxc export {containers[2]} ~/"`date +"%m%d%Y"`"_{containers[2]}.tar.xz --optimized-storage""")                                
                except:
                    current_app.logger.debug(f"An error occured while saving container {container}, swapping to next one")
                    continue

    except Exception as e:
        current_app.logger.error(f"An error occured while reaching endpoint {ENDPOINT}/backup : {e}")
        return e
    finally:
        handler.close()

    return ""
