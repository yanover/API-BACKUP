from paramiko import (
    SSHClient,
    AutoAddPolicy,
    AuthenticationException,
    SSHException,
)

from common.errors.HttpExceptions import AuthException, SshException

from flask import current_app

class CommandException(Exception):
    pass

class SSH:
    def __init__(self, host, user, password):
        self.handler = None
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.handler = SSHClient()
            self.handler.set_missing_host_key_policy(AutoAddPolicy())
            self.handler.connect(
                hostname=self.host, username=self.user, password=self.password
            )
        except AuthenticationException as authenticationException:
            current_app.logger.debug("Authentication failed, please verify your credentials: %s")
            raise AuthException()
        except SSHException as sshException:
            current_app.logger.debug("Unable to establish SSH connection: %s" % sshException)
            raise SshException

    def send(self, cmd):
        current_app.logger.debug(f"Sending command : {cmd}")
        try:
            stdin, stdout, stderr = self.handler.exec_command(cmd)
            # store the stderr
            error = stderr.readlines()
            # create an entry for stderr that is pretty to read
            if(error):
                err = ("".join(error)).strip()
                raise CommandException(err)

            """ for line in iter(stdout.readline, ""):
                print(line, end="") """

        except SSHException as sshException:
            print("An error occured while sending command: %s" % sshException)
            raise(sshException)
        except Exception as e: 
            raise(e)


    def close(self):
        if self.handler is not None and self.handler.get_transport() is not None:
            current_app.logger.debug("Closing SSH session ..")
            self.handler.close()