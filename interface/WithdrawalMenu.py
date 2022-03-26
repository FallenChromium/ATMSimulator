from interface.AmountDialogue import amountDialogue
from interface.BaseMenu import BaseMenu
from rich.prompt import IntPrompt
from interface.ConfirmDialogue import confirmDialogue
from resources import IncorrectAmountValueException, NotEnoughFundsException
import utilities
import settings


class WithdrawalMenu(BaseMenu):
    def show(self):
            choice = amountDialogue("How much do you want to withdraw? 0 for exit")
            can_give = settings.atm.calculateWithdraw(choice)
            if (choice == 0): return
            else:
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
