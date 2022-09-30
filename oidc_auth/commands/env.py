from .. import config, database, plugins
from .login import main as login


def main(namespace, _):
    credentials = database.Credentials()
    token = credentials.get_token(namespace.provider_alias)
    if not token:
        login(namespace, _)
        token = credentials.get_token(namespace.provider_alias)

    provider = config.provider(namespace.provider_alias)
    for p in provider.plugins:
        plugin = plugins.get(p)
        plugin.print_actions(token, provider.plugins[p].options)
