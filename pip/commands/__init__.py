"""
Package containing all pip commands
"""
from __future__ import absolute_import

from pip.commands.completion import CompletionCommand
from pip.commands.freeze import FreezeCommand
from pip.commands.help import HelpCommand
from pip.commands.list import ListCommand
from pip.commands.search import SearchCommand
from pip.commands.show import ShowCommand
from pip.commands.install import InstallCommand
from pip.commands.uninstall import UninstallCommand
from pip.commands.unzip import UnzipCommand
from pip.commands.zip import ZipCommand
from pip.commands.wheel import WheelCommand

import sys

thismodule = sys.modules[__name__]

_commands = {
    CompletionCommand.name: CompletionCommand,
    FreezeCommand.name: FreezeCommand,
    HelpCommand.name: HelpCommand,
    SearchCommand.name: SearchCommand,
    ShowCommand.name: ShowCommand,
    InstallCommand.name: InstallCommand,
    UninstallCommand.name: UninstallCommand,
    UnzipCommand.name: UnzipCommand,
    ZipCommand.name: ZipCommand,
    ListCommand.name: ListCommand,
    WheelCommand.name: WheelCommand,
}


commands_order = [
    InstallCommand,
    UninstallCommand,
    FreezeCommand,
    ListCommand,
    ShowCommand,
    SearchCommand,
    WheelCommand,
    ZipCommand,
    UnzipCommand,
    HelpCommand,
]



import collections
import collections.abc

class commands(collections.abc.Iterable):
    """
    Define a local class to be instanciated and swap for the module defnition
    in sys  path at the end, it is the recommended way to fake a getattr on a
    module.
    """

    @classmethod
    def get_summaries(ignore_hidden=True, ordered=True):
        """Yields sorted (command name, command summary) tuples."""

        if ordered:
            cmditems = _sort_commands(_commands, commands_order)
        else:
            cmditems = _commands.items()

        for name, command_class in cmditems:
            if ignore_hidden and command_class.hidden:
                continue

            yield (name, command_class.summary)

    @classmethod
    def get_similar_commands(name):
        """Command name auto-correct."""
        from difflib import get_close_matches

        name = name.lower()

        close_commands = get_close_matches(name, _commands.keys())

        if close_commands:
            return close_commands[0]
        else:
            return False

    def __getattr__(self, key):
        return getattr(thismodule, key)

    def __getitem__(self, key):
        return _commands[key]

    def __iter__(self):
        self.it = iter(_commands)
        return self.it

    def __len__(self):
        return len(_commands)

    def __next__(self):
        return next(self.it)


def _sort_commands(cmddict, order):
    def keyfn(key):
        try:
            return order.index(key[1])
        except ValueError:
            # unordered items should come last
            return 0xff

    return sorted(cmddict.items(), key=keyfn)


sys.modules[__name__] = commands()
