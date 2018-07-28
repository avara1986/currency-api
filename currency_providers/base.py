from importlib import import_module
from typing import Text


class Provider(object):

    def __init__(self, provider: Text, base: Text):
        driver_module = 'currency_providers.providers.{}.driver'.format(provider)
        try:
            module = import_module(driver_module)
        except ImportError:
            raise ImportError('Driver %s not found', provider)
        else:
            self.provider = module.Driver(base=base)

    def get_provider(self):
        return self.provider


def provider(provider: Text, base: Text) -> Provider:
    provider = Provider(provider, base)
    return provider.get_provider()
