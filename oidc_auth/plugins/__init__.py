import os
import importlib


def get(name):
    module = importlib.import_module(f'.{name}', 'oidc_auth.plugins')
    return module.Plugin()


def available_plugins():
    plugins_dir = os.path.dirname(__file__)
    return [
        f.removesuffix('.py')
        for f in os.listdir(plugins_dir)
        if not f.startswith('_')
    ]
