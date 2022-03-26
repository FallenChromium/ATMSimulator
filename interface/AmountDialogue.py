from rich.prompt import IntPrompt
from interface.ConfirmDialogue import confirmDialogue
from resources import IncorrectAmountValueException, NotEnoughFundsException
import utilities

def amountDialogue(msg: str) -> int:
    while True:
            choice = IntPrompt.ask(
                msg)
            try:
                utilities.validateAmount(choice)
            except IncorrectAmountValueException:
                print("Duh, incorrect amount")
            else:
                return choice