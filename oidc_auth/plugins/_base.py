from abc import ABC, abstractmethod


class Plugin(ABC):

    def __init__(self):
        pass

    @property
    def name(self):
        return self._name()

    @abstractmethod
    def _name(self):
        pass

    @abstractmethod
    def prepare_environment(self, id_token, options):
        '''Prepares the Python environment prior to running a sub-shell.'''
        pass

    @abstractmethod
    def get_options_config(self):
        '''Gets a list of tuples describing the plugin options to set.

        Each tuple should be in the format (option_name, short_description). The short description
        will be used to generate the question shown to the usaer during configuration.
        '''
        pass
# TODO: Hook functions for writing and retrieving properties from providers file.
# TODO: Function to get script that configures the caller's environment.
