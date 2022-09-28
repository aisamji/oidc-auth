import os
import tempfile
from . import _base


class Plugin(_base.Plugin):

    def _name(self):
        return 'aws'

    def __del__(self):
        if hasattr(self, '_path'):
            os.remove(self._path)

    def prepare_environment(self, id_token, options):
        _, token_path = tempfile.mkstemp()
        self._path = token_path
        with open(self._path, 'w') as file:
            file.write(id_token)
        os.environ['AWS_WEB_IDENTITY_TOKEN_FILE'] = self._path

        os.environ['AWS_ROLE_ARN'] = options['role_arn']

    def get_options_config(self):
        return [
            ('role_arn', 'IAM Role to Assume'),
        ]
