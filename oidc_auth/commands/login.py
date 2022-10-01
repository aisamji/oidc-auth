import webbrowser
from urllib import parse as urlparse
from multiprocessing import Process, Pipe
import json
import requests
import logging
import random
from .. import config, database
from . import _server

LOGGER = logging.Logger(__name__)

CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'


def main(namespace, _):
    credentials = database.Credentials()
    id_token = credentials.get_token(namespace.provider_alias)
    if id_token:
        return id_token

    provider = config.provider(namespace.provider_alias)
    auth_request_uri, state = craft_request_uri(provider)
    conn, child_conn = Pipe()
    p = Process(target=_server.callback, args=(child_conn, state))
    p.start()
    webbrowser.open(auth_request_uri)
    code = conn.recv()
    id_token = get_id_token(provider, code)
    credentials.save_token(namespace.provider_alias, id_token)


def craft_request_uri(provider):
    endpoint = provider.authorization_endpoint
    random_state = ''.join([random.choice(CHARACTERS) for i in range(16)])
    query = urlparse.urlencode({
        'response_type': 'code',
        'client_id': provider.client_id,
        'redirect_uri': 'http://localhost:9527/code',
        'state': random_state,
        'scope': 'openid',
    })
    return f'{endpoint}?{query}', random_state


def get_id_token(provider, code):
    query = {
        'grant_type': 'authorization_code',
        'client_id': provider.client_id,
        'client_secret': provider.client_secret,
        'code': code,
        'redirect_uri': 'http://localhost:9527/code',
    }
    response = requests.post(provider.token_endpoint, data=query)
    return json.loads(response.text)['id_token']
