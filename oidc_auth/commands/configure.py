from .. import config, plugins


def main(namespace, _):
    provider = config.provider(namespace.provider_alias)

    issuer_url = input(f'Issuer URL ({provider.issuer_url}): ')
    if issuer_url:
        provider.issuer_url = issuer_url

    client_id = input(f'Client ID ({provider.client_id}): ')
    if client_id:
        provider.client_id = client_id

    client_secret = input(f'Client Secret ({provider.client_secret}): ')
    if client_secret:
        provider.client_secret = client_secret

    available_plugins = plugins.available_plugins()
    while True:
        print('(0) Done')
        for i in range(len(available_plugins)):
            print(f'({i+1}) {available_plugins[i]}')

        try:
            response = int(input('Would you like to configure any additional plugins? '))
            if response > len(available_plugins):
                raise ValueError()
            if response == 0:
                break

            plugin = plugins.get(available_plugins[response-1])

            plugin_config = provider.plugins[plugin.name].options
            for attr, prompt in plugin.get_options_config():
                value = input(f'{prompt} ({plugin_config.get(attr, None)}): ')
                if value:
                    plugin_config[attr] = value

            provider.add_plugin(plugin.name)
            provider.plugins[plugin.name].options = plugin_config
        except ValueError:
            print('Please enter a valid integer in the above range.')
            continue

    config.save()
