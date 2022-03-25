from interface.BaseMenu import BaseMenu
import settings

class ShowBalanceMenu(BaseMenu):
    def show(self):
        bankname = settings.atm._card._emitent
        accountId = settings.atm._card.getBankAccountId()
        bank = next((bank for bank in settings.banks if bank.name == bankname))
        print("Your balance is: ", bank.getAccountBalance(accountId))


showBalanceMenu = ShowBalanceMenu({})
