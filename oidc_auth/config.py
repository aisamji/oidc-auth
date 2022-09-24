import os
import logging
from configparser import ConfigParser
import json
from urllib import parse as urlparse
import requests

LOGGER = logging.Logger(__name__)

_default_config_file = '~/.config/oidc-auth/providers'
_config_file = os.path.expanduser(os.environ.get('OIDC_AUTH_CONFIG_FILE', _default_config_file))

_parser = ConfigParser()
_parser.read(_config_file)


def save():
    with open(_config_file, 'w') as file:
        _parser.write(file)


def provider(alias, create=True):
    if create and not _parser.has_section(alias):
        _parser.add_section(alias)
    try:
        return _Provider(_parser[alias])
    except KeyError:
        LOGGER.fatal(f'Provider {alias!r} not found. Please ensure the config file exists and is properly formatted.')
        exit(1)


class _Provider:

    def __init__(self, section):
        self._section = section

    @property
    def alias(self):
        return self._section.name

    @property
    def issuer_url(self):
        return self._get_key('issuer_url')

    @issuer_url.setter
    def issuer_url(self, value):
        self._set_key('issuer_url', value)

    @property
    def client_id(self):
        return self._get_key('client_id')

    @client_id.setter
    def client_id(self, value):
        self._set_key('client_id', value)

    @property
    def client_secret(self):
        return self._get_key('client_secret')

    @client_secret.setter
    def client_secret(self, value):
        self._set_key('client_secret', value)

    def _get_key(self, key):
        try:
            return self._section[key]
        except KeyError:
            return None

    def _set_key(self, key, value):
        self._section[key] = str(value)

    @property
    def openid_configuration(self):
        url = urlparse.urljoin(self.issuer_url, '.well-known/openid-configuration')
        try:
            response = requests.get(url)
            return json.loads(response.text)
        except requests.exceptions.RequestException:
            LOGGER.fatal(f'No OpenID configuration found for {self.issuer_url}')
            exit(1)

    @property
    def jwks_uri(self):
        return self.openid_configuration['jwks_uri']

    @property
    def json_web_keyset(self):
        url = self.openid_configuration['jwks_uri']
        try:
            response = requests.get(url)
            keys = json.loads(response.text)
            return {k['kid']: _JsonWebKey(k) for k in keys['keys']}
        except requests.exceptions.RequestException:
            LOGGER.fatal(f'Could not retrieve JSON web keys for {self.issuer_url}')
            exit(1)

    @property
    def authorization_endpoint(self):
        return self.openid_configuration['authorization_endpoint']

    @property
    def token_endpoint(self):
        return self.openid_configuration['token_endpoint']


class _JsonWebKey:

    def __init__(self, key_json):
        self._json = key_json

    @property
    def algorithm(self):
        return self._json['alg']

    @property
    def json(self):
        return self._json
