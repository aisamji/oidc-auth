import argparse
import sys
import os
import logging
from .config import Config


LOGGER = logging.Logger(__name__)
DEFAULT_CONFIG_FILE = os.path.expanduser('~/.config/oidc-auth/providers')
CONFIG_FILE = os.environ.get('OIDC_AUTH_CONFIG_FILE', DEFAULT_CONFIG_FILE)
CONFIG = Config(CONFIG_FILE)


def main():
    args, command = extract_parts(sys.argv)
    parser = create_parser()
    ns = parser.parse_args(args)

    if ns.configure:  # We only want to configure the provider
        set_provider(ns.provider_alias)
    else:
        provider = get_provider(ns.provider_alias)

        if len(command) == 0:
            print_environment_configuration(provider)
        else:
            configure_python_environment(provider)
            os.system(' '.join(command))


def extract_parts(args):
    try:
        prefix_position = args.index('--')
        unescaped_command = args[prefix_position+1:]
        command = [repr(a) for a in unescaped_command]
        return (args[1:prefix_position], command)
    except ValueError:
        return (args[1:], [])


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--provider', dest='provider_alias', default='default')
    parser.add_argument('-c', '--configure', action='store_true')

    return parser


def get_provider(alias):
    try:
        return CONFIG.provider(alias, create=False)
    except KeyError:
        LOGGER.fatal(f'Provider {alias!r} not found. Please ensure the config file exists and is properly formatted.')
        exit(1)


def set_provider(alias):
    p = CONFIG.provider(alias)
    p.issuer_url = input(f'Issuer URL ({p.issuer_url}): ')
    p.client_id = input(f'Client ID ({p.client_id}): ')
    p.client_secret = input(f'Client Secret ({p.client_secret}): ')
    CONFIG.save()


def print_environment_configuration(provider):
    # print exports and aliases
    pass


def configure_python_environment(provider):
    pass
