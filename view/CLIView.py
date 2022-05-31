from utilities import validatePIN
from view.IView import IView
from resources import AuthenticationRequiredException, CardAlreadyInsertedException, CardIsLockedException, CardNotFoundException, IncorrectAmountValueException, IncorrectPINException, InvalidPINException, IncorrectPhoneNumberException, NotEnoughFundsException
import settings
# For some sweet UI elements
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
# CLI arguments parsing
import typer

class CLIView(IView):
    def __init__(self, controller):
        super().__init__(controller)
        self.cli_controller = controller
        self.app = typer.Typer()

        self.register_command(self.logout)
        self.register_command(self.login)
        self.register_command(self.cards)
        self.register_command(self.show_balance)
        self.register_command(self.phone_topup)
        self.register_command(self.withdraw)

    def start_atm(self):
        self.app()

    def logout(self):
        self.cli_controller.logout()

    # there should be proper error handling, but it kinda doesn't matter in the CLI app, does it?
    def login(self, card: int):
        try:
            self.cli_controller.loginGuard(card)
        except CardAlreadyInsertedException as e:
            print(e)
        except CardNotFoundException as e:
            print(e)
        else:
            try:
                self.cli_controller.login(card, CLIView.enterPin())
            except CardIsLockedException as e:
                print(e)
                quit()
            except IncorrectPINException as e:
                print(e)

    def cards(self):
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
            except InvalidPINException:
                print("Invalid input!")
                continue
            
            return pin

    def show_balance(self):
        try:
            print(self.cli_controller.getBalance())
        except AuthenticationRequiredException as error:
            print(error)

    def withdraw(self, amount: float):
        try:
            self.cli_controller.withdrawConfirmation(amount)            
        except NotEnoughFundsException as error:
            print(error)
        except AuthenticationRequiredException as error:
            print(error)

    def withdrawSummary(self, amount):
        cash = self.cli_controller.withdraw(amount)
        for banknote in cash:
            print(banknote)
    
    def withdrawConfirmation(self, dialog_text: str, amount: float):
        if typer.confirm(dialog_text):
            self.withdrawSummary(amount)


    def register_command(self, func):
        self.app.command()(func)

    def phone_topup(self, phone: str, amount: str):
        try:
            self.cli_controller.phoneTopup(phone, float(amount))
        except IncorrectPhoneNumberException as error:
            print(error)
        except IncorrectAmountValueException as error:
            print(error)
        except NotEnoughFundsException as error:
            print(error)
        # conversion error
        except ValueError:
            print(IncorrectAmountValueException())
        except AuthenticationRequiredException as error:
            print(error)

