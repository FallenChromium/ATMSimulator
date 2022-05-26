from utilities import validatePIN
from view.IView import IView
from resources import CardAlreadyInsertedException, IncorrectAmountValueException, IncorrectPINException, IncorrectPhoneNumberException, NotEnoughFundsException
import settings
# For some sweet UI elements
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
# CLI arguments parsing
import click

class CLIView(IView):
    def __init__(self, controller):
        # an awful workaround for Click's inability to use object's methods as commands
        # Set cli_controller global variable and use it rather than self.controller which is the default behavior for views
        super().__init__(controller)
        global cli_controller
        cli_controller = controller

    @click.group()
    @staticmethod
    def atm():
        pass

    @atm.command('logout')
    @staticmethod
    def logout():
        cli_controller.logout()

    @atm.command('insert')
    @click.argument('card', type=click.INT)
    @staticmethod
    def login(card):
        try:
            cli_controller.login(card)
        except CardAlreadyInsertedException as e:
            print(e)

    @atm.command('cards')
    @staticmethod
    def show_available_cards():
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Index", style="dim")
        table.add_column("Number", style="dim")
        for idx, card in enumerate(settings.cards):
            table.add_row(str(idx), card._cardNumber)
        console.print(table)
        exit(0)


    @classmethod
    def enterPin(cls) -> str:
        while True:
            pin = Prompt.ask(
                "[cyan]Please enter PIN",
                password=True,
            )
            # Validate PIN first
            try:
                validatePIN(pin)
            except IncorrectPINException:
                print("Invalid input!")
                continue
            
            return pin

    @atm.command('show_balance')
    @staticmethod
    def show_balance():
        try:
            print(cli_controller.getCardBalance())
        except Exception as error:
            print(error)

    @atm.command('withdraw')
    @click.argument('amount')
    @staticmethod
    def withdraw(amount):
        try:
            cash = cli_controller.withdraw(float(amount))
        except NotEnoughFundsException as error:
            print(error)
        else:
            for banknote in cash:
                print(banknote)
    
    def confirmation(self, dialog_text: str):
        return click.confirm(dialog_text)

    @atm.command('phone_topup')
    @click.argument('phone')
    @click.argument('amount')
    @staticmethod
    def phone_topup(phone, amount):
        try:
            cli_controller.phoneTopup(phone, float(amount))
        except IncorrectPhoneNumberException as error:
            print(error)
        except IncorrectAmountValueException as error:
            print(error)
        except ValueError:
            print(IncorrectAmountValueException())

