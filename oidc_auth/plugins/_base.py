import shutil
import tempfile
from abc import ABC, abstractmethod


class Plugin(ABC):

    def __init__(self):
        pass

    def __del__(self):
        if hasattr(self, '_tempdir'):
            shutil.rmtree(self._tempdir)

    @property
    def name(self):
        return self._name()

    @abstractmethod
    def _name(self):
        pass

    @abstractmethod
    def get_options_config(self):
        '''Gets a list of tuples describing the plugin options to set.

        Each tuple should be in the format (option_name, short_description). The short description
        will be used to generate the question shown to the usaer during configuration.
        '''
        pass

    def prepare_environment(self, id_token, options):
        '''Prepares the Python environment prior to running a sub-shell.'''
        if hasattr(self, '_tempdir'):
            shutil.rmtree(self._tempdir)
        self._tempdir = tempfile.mkdtemp()
        actions = self._get_actions(id_token, options, self._tempdir)
        actions.execute()

    def print_actions(self, id_token, options):
        actions = self._get_actions(id_token, options, '.')
        actions.print()

    @abstractmethod
    def _get_actions(self, id_token, options, directory):
        '''Get a list of Instruction objects specifying how to configure the environment.'''
        pass
