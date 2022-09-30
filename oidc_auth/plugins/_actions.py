import os
import re
import random
from abc import ABC, abstractmethod


def _generate_random_alphanum():
    alphanum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choices(alphanum, k=15))


class ActionList:

    def __init__(self, actions):
        self._actions = actions

    def execute(self):
        self._on_each('execute')

    def print(self):
        self._on_each('print')

    def _on_each(self, func):
        substitutions = {}

        for act in self._actions:
            function = getattr(act, func)
            result = function(substitutions)
            if act.name != '':
                substitutions[act.name] = result


class _BaseAction(ABC):

    _required_args = []
    _optional_args = {}

    def __init__(self, **kwargs):
        for a in self._required_args:
            if a not in kwargs:
                raise TypeError(f'Missing 1 keyword argument: {a!r}')
        for a in kwargs:
            if a not in self._required_args and a not in self._optional_args and a != 'name':
                raise TypeError(f'Got an unexpected keyword argument {a!r}')

        self._args = kwargs
        for a, d in self._optional_args.items():
            if a not in self._args:
                self._args[a] = d if not callable(d) else d()
        if 'name' not in self._args:
            self._args['name'] = ''  # Default save as name

    def __getattr__(self, attr):
        try:
            return self._args[attr]
        except KeyError:
            raise AttributeError()

    def execute(self, substitutions):
        self._make_substitutions(substitutions)
        return self._execute()

    @abstractmethod
    def _execute(self):
        pass

    def print(self, substitutions):
        self._make_substitutions(substitutions)
        return self._print()

    @abstractmethod
    def _print(self):
        pass

    def _make_substitutions(self, substitutions):
        re_substitutions = {
            rf'\${k}': v
            for k, v in substitutions.items()
        }
        for attr, val in self._args.items():
            for pattern, repl in re_substitutions.items():
                self._args[attr] = re.sub(pattern, repl, str(val))


class CreateFileAction(_BaseAction):

    _required_args = [
        'dirname',
        'content',
    ]

    _optional_args = {
        'filename': _generate_random_alphanum,
    }

    def _execute(self):
        filepath = os.path.join(self.dirname, self.filename)
        with open(filepath, 'w') as file:
            file.write(self.content)
        return filepath

    def _print(self):
        filepath = os.path.join(self.dirname, self.filename)
        print(f"echo '{self.content}' > {filepath}")
        return filepath


class SetEnvironmentAction(_BaseAction):

    _required_args = [
        'variable',
        'value',
    ]

    def _execute(self):
        os.environ[self.variable] = self.value
        return self.variable

    def _print(self):
        print(f"export {self.variable}='{self.value}'")
        return self.variable
