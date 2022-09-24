import os
import sqlite3
import logging
import jwt
from jwt import PyJWKClient
from .. import config

LOGGER = logging.Logger(__name__)


class Credentials:

    DESIRED_VERSION = 1
    MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations')

    def __init__(self):
        pardir = os.path.dirname(config._config_file)
        os.makedirs(pardir, exist_ok=True)
        file = os.path.join(pardir, 'credentials.db')
        self._db = sqlite3.connect(file)
        self._update_version()

    def _update_version(self):
        if self.version == Credentials.DESIRED_VERSION:
            return
        if self.version > Credentials.DESIRED_VERSION:
            LOGGER.fatal('credentials.db file is using an unsupported version of the schema.')
            exit(1)

        for num in range(self.version + 1, Credentials.DESIRED_VERSION + 1):
            self._execute_migration(os.path.join(Credentials.MIGRATIONS_DIR, f'v{num}.sql'))
            self._db.execute(f'PRAGMA user_version={num}')
            self._db.commit()

    @property
    def version(self):
        return self._db.execute('PRAGMA user_version').fetchone()[0]

    def _execute_migration(self, path):
        with open(path) as file:
            script = file.read()
        self._db.executescript(script)

    def save_token(self, alias, id_token):
        self._validate_token(alias, id_token)
        self._db.execute('INSERT OR REPLACE INTO tokens(provider, id_token) VALUES (?, ?)', (alias, id_token))
        self._db.commit()

    def get_token(self, alias):
        result = self._db.execute(
                'SELECT id_token FROM tokens WHERE provider = ?',
                (alias,)
            ).fetchone()
        if result:
            try:
                self._validate_token(alias, result[0])
                return result[0]
            except jwt.exceptions.PyJWTError:
                return None
        else:
            return None

    @staticmethod
    def _validate_token(alias, id_token):
        # https://auth0.com/docs/quickstart/backend/python/01-authorization#validate-access-tokens
        provider = config.provider(alias)
        header = jwt.get_unverified_header(id_token)
        algorithm = header['alg']
        jwks_client = PyJWKClient(provider.jwks_uri)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        jwt.decode(
            id_token,
            signing_key.key,
            algorithms=[algorithm],
            audience=provider.client_id,
            issuer=provider.issuer_url
        )
