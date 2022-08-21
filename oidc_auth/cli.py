import argparse
import sys
import os


def main():
    args, command = extract_parts(sys.argv)
    parser = create_parser()
    parser.parse_args(args)

    if len(command) == 0:
        print_environment_configuration()
    else:
        configure_python_environment()
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

    return parser


def get_oidc_parameters():
    pass


def print_environment_configuration():
    print('export')
    print('alias')


def configure_python_environment():
    pass
