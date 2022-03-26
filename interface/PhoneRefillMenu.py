from interface.AmountDialogue import amountDialogue
from interface.BaseMenu import BaseMenu
from interface.ConfirmDialogue import confirmDialogue
from rich.prompt import Prompt
from resources import NotEnoughFundsException
import settings
import utilities
from resources import IncorrectPhoneNumberException

class PhoneRefillSumMenu(BaseMenu):
    def show(self):
            choice = amountDialogue("How much do you want to put on your phone? 0 for exit")
            if (choice == 0): return
            else:
                    try:
                        settings.atm.bank.withdrawFromAccount(
                            settings.atm.accountId, choice)
                    except NotEnoughFundsException:
                        print("Nah man, you don't have that much")
                    else:
                        print("You topped up your phone! Amount: ", str(choice)) 
                        return


phoneRefillSumMenu = PhoneRefillSumMenu({})

def phoneDialogue(msg: str):
    while True:
            choice = Prompt.ask(
                msg)
            try:
                utilities.validatePhone(choice)
            except IncorrectPhoneNumberException as exception:
                print(exception)
            else:
                return choice
class PhoneRefillMenu(BaseMenu):
    def show(self):
            phone = phoneDialogue("Enter your phone number. 0 for exit")
            if (phone == 0): return
            else:
                if(confirmDialogue("Your phone is: " + str(phone) + ". Is that alright?")):
                        phoneRefillSumMenu.show()
                        return


phoneRefillMenu = PhoneRefillMenu({})