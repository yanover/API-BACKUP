from flask import Blueprint, request, abort, current_app
from models.Stack import Stack
from PyMySQL import _mysql

# Declare Blueprint
database_endpoint = Blueprint("database_endpoint", __name__)

# Route default path
ENDPOINT = '/mysql'

# In memory Pile
stack = Stack()


@database_endpoint.route(ENDPOINT, methods=['GET'])
def default():
    current_app.logger.debug('Retrieve backups')
    return str(stack.peek())


@database_endpoint.route(f"{ENDPOINT}/backup", methods=['GET'])
def min():
    return str(stack.min())