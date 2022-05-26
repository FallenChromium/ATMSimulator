from model.ATM import ATM
from resources import CardAlreadyInsertedException
import settings
from utilities import validatePIN, validatePhone
from view.CLIView import CLIView
class ATMController:
    def __init__(self, ATM: ATM):
        self.atm = ATM

    def startUI(self, variation: str):
        if variation == "gui":
            pass
        if variation == "cli":
            self.view = CLIView(self)
        self.view.atm()

    def logout(self):
        self.atm.logout()

    def login(self, card_index):
        if self.isCardInserted():
            raise CardAlreadyInsertedException
        while True:
            pin = self.view.enterPin()
            validatePIN(pin)
            if settings.cards[card_index].unlockCard(pin):
                self.atm.authenticate(card_index)
                break

    def getCardBalance(self) -> float:
        return self.atm.getBank().getAccountBalance(self.atm.getAccountId())

    def phoneTopup(self, phone: str, amount: float):
        validatePhone(phone)
        self.atm.getBank().withdrawFromAccount(self.atm.getAccountId(), amount)
        # We are supposed to top up a phone, but why would we simulate any? 
        # It's an ATM simulator, not carrier simulator...

    def withdraw(self, amount: float) -> list[str]:
        real_amount = self.atm.calculateWithdraw(amount)
        if real_amount == amount:
            self.atm.getBank().withdrawFromAccount(self.atm.getAccountId(), amount)
            return self.atm.withdraw(amount)
        else:
            if self.view.confirmation("Best we can do is " + str(real_amount) + ", is that okay?"):
                self.atm.getBank().withdrawFromAccount(self.atm.getAccountId(), real_amount)
                return self.atm.withdraw(real_amount)
            # else (if the possible sum is not okay) - do nothing
            else: 
                print("Well...")
                return []

    def isCardInserted(self) -> bool:
        return self.atm.isCardInserted()