import abc
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import types


class BaseMenu(abc.ABC):
    # int -> button in the interface; function -> action called; str -> description of the action.
    __actions: dict[str, tuple[types.FunctionType, str]]

    def action(self, input):
        choices = list(self.__actions.keys())
        choice = Prompt.ask("What do you want to do?", choices=choices)
        self.__actions[choice][0]()

    def show(self):
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Button", style="dim", width=12)
        table.add_column("Action", style="dim", width=12)
        for key, value in self.__actions.items():
            table.add_row(str(key), value[1])
        console.print(table)
