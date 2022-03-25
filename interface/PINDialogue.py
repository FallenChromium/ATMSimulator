from Bank import Card
from utilities import validatePIN
from resources import IncorrectPINException, CardIsLockedException
from interface.MainMenu import MainMenu
from rich.prompt import Prompt
import settings


def PINDialogue() -> None:
    while True:
        pin = Prompt.ask(
            "[cyan]Please enter PIN (0 for exit)",
            password=True,
        )
        if (pin == "0"):
            return
        # Validate PIN first
        try:
            validatePIN(pin)
        except IncorrectPINException:
            print("[prompt.invalid]Invalid input!")
            continue
        # Then fall into main menu unless the password is incorrect or the card is locked
        try:
            if(settings.atm._card.unlockCard(pin)):
                MainMenu().show()
        except CardIsLockedException:
            print(CardIsLockedException.__str__)
            return
