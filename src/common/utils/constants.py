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

        def transform(cmd, patterns, values, idx = 0):
            if len(patterns) <= idx or idx > len(patterns): return cmd
            return transform(
                cmd.replace(f"%{patterns[idx]}%", values[idx]),
                patterns, values, idx +  1
            )

        self.APP_CMDS = {
            "TRANSFORMER": transform,
            "DB": {
                "MOVE": f"cd {self.APP_CONFIG['NAS_DEST']}/database;ls -alh --fu | grep '^-'",
                "FILENAME": f"{self.APP_CONFIG['PI_SRC']}/%time%_%db%.sql.gz",
                "DUMP": f"mysqldump -u {self.APP_CONFIG['MYSQL_USER']} -p{self.APP_CONFIG['MYSQL_PASS']} %db% | gzip -c > %filename%;",
                "COPY": f"sshpass -p '{self.APP_CONFIG['NAS_PASS']}' scp %filename% ${self.APP_CONFIG['NAS_USER']}@{self.APP_CONFIG['NAS_HOST']}:{self.APP_CONFIG['NAS_DEST']}/database"
           },
           "CONTAINER": {
               "GET": "/snap/bin/lxc ls -c n --format csv",
               "MOVE": f"cd {self.APP_CONFIG['NAS_DEST']}/containers;ls -alh --fu | grep '^-'",
               "FILENAME": f"{self.APP_CONFIG['PI_SRC']}/%time%_%container%.tar.xz",
               "DUMP":  f"/snap/bin/lxc export %container% %filename% --optimized-storage",
               "COPY": f"sshpass -p '{self.APP_CONFIG['NAS_PASS']}' scp %filename%  {self.APP_CONFIG['NAS_USER']}@{self.APP_CONFIG['NAS_HOST']}:{self.APP_CONFIG['NAS_DEST']}/database"
           }
        }