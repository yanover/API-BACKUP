from paramiko import (
    SSHClient,
    AutoAddPolicy,
    AuthenticationException,
    BadHostKeyException,
    SSHException,
)


class SSH:
    def __init__(self, host, user, password):
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
            print("Authentication success")
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)

    def send(self, cmd):
        try:
            stdin, stdout, stderr = self.handler.exec_command(cmd)
            
            for line in iter(stdout.readline, ""):
                print(line, end="")

        except SSHException as sshException:
            print("An error occured while sending command: %s" % sshException)
