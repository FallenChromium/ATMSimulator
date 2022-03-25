from interface.BaseMenu import BaseMenu
from rich.prompt import IntPrompt
from interface.ConfirmDialogue import confirmDialogue
from resources import IncorrectAmountValueException, NotEnoughFundsException
import utilities
import settings


class WithdrawalMenu(BaseMenu):
    def show(self):
        while True:
            choice = IntPrompt.ask(
                "Enter the amount you want to withdraw (0 to go back)")
            if (choice == 0): return
            try:
                utilities.validateAmount(choice)
            except IncorrectAmountValueException:
                print("Duh, incorrect amount")
            else:
                can_give = settings.atm.calculateWithdraw(choice)
                if(confirmDialogue("Best we can do for you is " + str(can_give) + ". Is that alright?")):
                    try:
                        settings.atm.bank.withdrawFromAccount(
                            settings.atm.accountId, can_give)
                    except NotEnoughFundsException:
                        print("Nah man, you don't have that much")
                    else:
                        settings.atm.withdraw(can_give)
                        return


withdrawalMenu = WithdrawalMenu({})
