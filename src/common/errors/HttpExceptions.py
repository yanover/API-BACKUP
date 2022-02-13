from werkzeug.exceptions import HTTPException, NotFound

class LogError(HTTPException):
    code = 400
    description = 'An error occured while sending log'

class SshException(HTTPException):
    code = 400
    description = 'Unable to establish SSH connection'
    
class AuthException(HTTPException):
    code = 401
    description = 'Authentication failed, please verify your credentials'


