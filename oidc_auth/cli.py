import argparse
import sys
import logging
from . import commands

LOGGER = logging.Logger(__name__)


def main():
    args, command = extract_parts(sys.argv)
    parser = create_parser()
    ns = parser.parse_args(args)

    if ns.func:
        ns.func(ns, command)
    else:
        parser.print_help()


def extract_parts(args):
    try:
        prefix_position = args.index('--')
        unescaped_command = args[prefix_position+1:]
        command = [a for a in unescaped_command]
        return (args[1:prefix_position], command)
    except ValueError:
        return (args[1:], [])


def create_parser():
    # Global Options
    global_parser = argparse.ArgumentParser(add_help=False)
    global_flags = global_parser.add_argument_group('Global Flags')
    global_flags.add_argument(
        '-p', '--provider',
        dest='provider_alias',
        default='default',
        )

    # Root Parser
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)
    command_parsers = parser.add_subparsers(title='Commands')

    # Configure Command
    configure_command = command_parsers.add_parser(
        'configure',
        parents=[global_parser]
        )
    configure_command.set_defaults(func=commands.configure)

    # Login Command
    login_command = command_parsers.add_parser(
        'login',
        parents=[global_parser]
    )
    login_command.set_defaults(func=commands.login)

    # Run Command
    run_command = command_parsers.add_parser(
        'run',
        parents=[global_parser]
    )
    run_command.set_defaults(func=commands.run)

    # ID-Token Command
    id_token_command = command_parsers.add_parser(
        'id-token',
        parents=[global_parser]
    )
    id_token_command.add_argument(
        '-d', '--decoded',
        action='store_true',
    )
    id_token_command.set_defaults(func=commands.id_token)

    return parser
