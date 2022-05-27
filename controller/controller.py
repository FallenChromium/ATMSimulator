from model.ATM import ATM
from resources import AuthenticationRequiredException, CardAlreadyInsertedException, CardNotFoundException, IncorrectPINException
import settings
from utilities import validateAmount, validatePIN, validatePhone

# a decorator for things which can only be called if you're authenticated
# adds accountId as the last argument to the function
# static method because python's syntactic sugar doesn't imply that you pass self to the decorator
def requires_auth(function):
    def wrapper_func(*args):
        # args[0] here is the "self" in the called function
        if args[0].atm.isCardInserted():
            return function(*args, lambda self=args[0]: self.atm.getAccountId())
        else: raise(AuthenticationRequiredException)
    return wrapper_func
class ATMController:



    def __init__(self, ATM: ATM):
        self.atm = ATM

    def startUI(self, variation: str):
        if variation == "gui":
            from view.GUIView import GUIView
            self.view = GUIView(self)
        if variation == "cli":
            from view.CLIView import CLIView
            self.view = CLIView(self)
        self.view.atm()

    def logout(self):
        self.atm.logout()

    def loginGuard(self, card_index: int):
        if self.isCardInserted():
            raise CardAlreadyInsertedException
        # if there's no card like this (as per EAFP codestyle)
        try:
            settings.cards[card_index]
        except IndexError:
            raise CardNotFoundException

    def login(self, card_index: int, pin: str):
            validatePIN(pin)
            if settings.cards[card_index].unlockCard(pin):
                self.atm.authenticate(card_index)
            else: 
                raise IncorrectPINException

    @requires_auth
    def getBalance(self,accountId) -> float:
        return self.atm.getBank().getAccountBalance(accountId())

    @requires_auth
    def phoneTopup(self, phone: str, amount: float, accountId):
        validatePhone(phone)
        amount = float(amount)
        validateAmount(amount)
        self.atm.getBank().withdrawFromAccount(accountId(), amount)
        # We are supposed to top up a phone, but why would we simulate any? 
        # It's an ATM simulator, not a mobile carrier simulator...

    @requires_auth
    def withdrawConfirmation(self, amount: float, accountId):
        amount = float(amount)
        validateAmount(amount)
        real_amount = self.atm.calculateWithdraw(amount)
        if real_amount != amount:
            self.view.withdrawConfirmation("Best we can do is " + str(real_amount) + ", is that okay?", real_amount)
        else: self.view.withdrawConfirmation("You are about to withdraw: " + str(amount) + ". Do you want to continue?", amount)

    @requires_auth
    def withdraw(self, amount: float, accountId) -> "list[str]":
            self.atm.getBank().withdrawFromAccount(accountId(), amount)
            cash = self.atm.withdraw(amount)
            return(cash)


    def isCardInserted(self) -> bool:
        return self.atm.isCardInserted()