import requests
import datetime
import time
from flask import current_app
from common.errors.HttpExceptions import LogError

class Log():
    def __init__(self, api_log, result, action, message, method, tagName):
        self.api_log = api_log
        self.json_playload = {
            'params': { 
                'result': result, 
                'action': action,
                'message': message,
                'method': method,
                'created': self.get_date(),
                'tagName': tagName  
            }
        }

    def log(self):
        current_app.logger.debug(f"Sending log to {self.api_log}")
        try:
            r = requests.post(self.api_log, json=self.json_playload)
            r.raise_for_status()
        except requests.exceptions.RequestException as e: 
            raise LogError()

    def get_date(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')