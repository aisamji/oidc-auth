import json
import jwt
from .. import database
from .login import main as login


def main(namespace, _):
    credentials = database.Credentials()
    token = credentials.get_token(namespace.provider_alias)
    if not token:
        login(namespace, _)
        token = credentials.get_token(namespace.provider_alias)

    # The token would already have been verified by this point.
    if namespace.decoded:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(json.dumps(decoded_token, indent=2))
    else:
        print(token)
