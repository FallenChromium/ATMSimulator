from model.ATM import ATM
from resources import AuthenticationRequiredException, CardAlreadyInsertedException
import settings
from utilities import validatePIN, validatePhone
from view.CLIView import CLIView

class ATMController:

    # a decorator for things which can only be called if you're authenticated
    # adds accountId as the last argument to the function
    # static method because python's syntactic sugar doesn't imply that you pass self to the decorator
    @staticmethod
    def requires_auth(function):
        def wrapper_func(*args):
            # args[0] here is the "self" in the called function
            if args[0].atm.isCardInserted():
                function(*args, args[0].atm.getAccountId())
            else: raise(AuthenticationRequiredException)
        return wrapper_func

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

    def login(self, card_index: int):
        if self.isCardInserted():
            raise CardAlreadyInsertedException
        while True:
            pin = self.view.enterPin()
            validatePIN(pin)
            if settings.cards[card_index].unlockCard(pin):
                self.atm.authenticate(card_index)
                break

    @requires_auth
    def getCardBalance(self,accountId: str) -> float:
        return self.atm.getBank().getAccountBalance(accountId)

    @requires_auth
    def phoneTopup(self, phone: str, amount: float, accountId: str):
        validatePhone(phone)
        self.atm.getBank().withdrawFromAccount(accountId, amount)
        # We are supposed to top up a phone, but why would we simulate any? 
        # It's an ATM simulator, not a mobile carrier simulator...

    @requires_auth
    def withdraw(self, amount: float, accountId: str) -> list[str]:
        real_amount = self.atm.calculateWithdraw(amount)
        if real_amount == amount:
            self.atm.getBank().withdrawFromAccount(accountId, amount)
            return self.atm.withdraw(amount)
        else:
            if self.view.confirmation("Best we can do is " + str(real_amount) + ", is that okay?"):
                self.atm.getBank().withdrawFromAccount(accountId, real_amount)
                return self.atm.withdraw(real_amount)
            # else (if the possible sum is not okay) - do nothing
            else: 
                return []

    def isCardInserted(self) -> bool:
        return self.atm.isCardInserted()