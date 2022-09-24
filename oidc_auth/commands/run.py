import subprocess
import os
from .. import database
from .login import main as login


def main(namespace, command):
    if not command:
        print('A command is expected.')
        exit(1)

    credentials = database.Credentials()
    token = credentials.get_token(namespace.provider_alias)
    if not token:
        login(namespace, command)

    # @TODO: Configure environment for subprocess
    shell_command = os.path.expanduser(' '.join([repr(c) for c in command]))
    subprocess.run(shell_command, shell=True)
