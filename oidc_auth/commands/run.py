import subprocess
import os
from .. import config, database, plugins
from .login import main as login


def main(namespace, command):
    if not command:
        print('A command is expected.')
        exit(1)

    credentials = database.Credentials()
    token = credentials.get_token(namespace.provider_alias)
    if not token:
        login(namespace, command)
        token = credentials.get_token(namespace.provider_alias)

    # @TODO: Configure environment for subprocess
    provider = config.provider(namespace.provider_alias)
    for p in provider.plugins:
        plugin = plugins.get(p)
        plugin.prepare_environment(token, provider.plugins[p].options)

    shell_command = os.path.expanduser(' '.join([repr(c) for c in command]))
    subprocess.run(shell_command, shell=True)
