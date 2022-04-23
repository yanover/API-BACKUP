import os

class Constants:

    def __init__(self):
        self.init_app_config()
        self.init_cmds()

    def init_app_config(self):
        self.APP_CONFIG = {
            "BESPIN_HOST": os.environ.get("BESPIN_HOST"),
            "PI_USER": os.environ.get("PI_USER"),
            "PI_PASS": os.environ.get("PI_PASS"),
            "PI_SRC": os.environ.get("PI_SRC"),
            "MYSQL_USER": os.environ.get("MYSQL_USER"),
            "MYSQL_PASS": os.environ.get("MYSQL_PASS"),
            "NAS_HOST": os.environ.get("NAS_HOST"),
            "NAS_USER": os.environ.get("NAS_USER"),
            "NAS_PASS": os.environ.get("NAS_PASS"),
            "NAS_DEST": os.environ.get("NAS_DEST"),
            "API_LOG": os.environ.get("API_LOG")
        }

    def init_cmds(self):

        config = self.APP_CONFIG

        def transform(cmd, patterns, values):
            if not patterns: return cmd
            return transform(
                cmd.replace(f"%{patterns.pop(0)}%", values.pop(0)), patterns, values
            ) 

        self.APP_CMDS = {
            "TRANSFORMER": transform,
            "DB": {
                "MOVE": f"cd {config['NAS_DEST']}/database;ls -alh --fu | grep '^-'",
                "FILENAME": f"{config['PI_SRC']}/%time%_%db%.sql.gz",
                "DUMP": f"mysqldump -u {config['MYSQL_USER']} -p{config['MYSQL_PASS']} %db% | gzip -c > %filename%;",
                "COPY": f"sshpass -p '{config['NAS_PASS']}' scp %filename% ${config['NAS_USER']}@{config['NAS_HOST']}:{config['NAS_DEST']}/database"
           },
           "CONTAINER": {
               "GET": "/snap/bin/lxc ls -c n --format csv",
               "MOVE": f"cd {config['NAS_DEST']}/containers;ls -alh --fu | grep '^-'",
               "FILENAME": f"{config['PI_SRC']}/%time%_%container%.tar.xz",
               "DUMP":  f"/snap/bin/lxc export %container% %filename% --optimized-storage",
               "COPY": f"sshpass -p '{config['NAS_PASS']}' scp %filename%  {config['NAS_USER']}@{config['NAS_HOST']}:{config['NAS_DEST']}/database"
           }
        }