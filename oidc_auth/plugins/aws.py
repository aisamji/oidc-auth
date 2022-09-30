from . import _base, _actions


class Plugin(_base.Plugin):

    def _name(self):
        return 'aws'

    def get_options_config(self):
        return [
            ('role_arn', 'IAM Role to Assume'),
        ]

    def _get_actions(self, id_token, options, directory):
        return _actions.ActionList([
            _actions.CreateFileAction(dirname=directory, content=id_token, name='token_file'),
            _actions.SetEnvironmentAction(variable='AWS_WEB_IDENTITY_TOKEN_FILE', value='$token_file'),
            _actions.SetEnvironmentAction(variable='AWS_ROLE_ARN', value=options['role_arn']),
        ])
