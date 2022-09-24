from .. import config


def main(namespace, _):
    p = config.provider(namespace.provider_alias)

    issuer_url = input(f'Issuer URL ({p.issuer_url}): ')
    if issuer_url:
        p.issuer_url = issuer_url

    client_id = input(f'Client ID ({p.client_id}): ')
    if client_id:
        p.client_id = client_id

    client_secret = input(f'Client Secret ({p.client_secret}): ')
    if client_secret:
        p.client_secret = client_secret

    config.save()
