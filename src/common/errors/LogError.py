from werkzeug.exceptions import HTTPException, NotFound

class LogError(HTTPException):
    code = 400
    description = 'An error occured while sending log'