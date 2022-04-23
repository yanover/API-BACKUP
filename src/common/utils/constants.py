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
        self.APP_CMDS = {
            "GET_DATABASES_MOVE" : f"cd {self.APP_CONFIG['NAS_DEST']}/database;ls -alh --fu | grep '^-'",
            "SAVE_DATABASE_FILE" : f"{self.APP_CONFIG['PI_SRC']}/{now.strftime('%d%m%Y')}_{db}.sql.gz"
        }