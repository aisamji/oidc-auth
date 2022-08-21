from configparser import ConfigParser


class Config:

    def __init__(self, filepath):
        self._parser = ConfigParser()
        self._parser.read(filepath)  # Skips file if it does not exist.
        self._filepath = filepath

    def save(self):
        with open(self._filepath, 'w') as file:
            self._parser.write(file)

    def provider(self, alias, create=True):
        if create and not self._parser.has_section(alias):
            self._parser.add_section(alias)
        return Config._Provider(self._parser[alias])

    class _Provider:

        def __init__(self, section):
            self._section = section

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
