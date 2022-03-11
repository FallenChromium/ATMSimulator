import random
import string

from resources import *

#Utilities
def validatePIN(pin:str):
    if(len(pin) != 4): 
        raise IncorrectPINException
    for char in pin:
        if char not in string.digits:
            raise IncorrectPINException

def validateAmount(amount:int):
    if(amount < 0 or not isinstance(amount, int)):
        raise IncorrectAmountValueException


class BankAccount:
    _balance: int = 0
    _owner: str = ""

    def __init__(self, owner):
        self._balance: int = 0
        self._owner: str = owner

    def replenish(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if self._balance - amount < 0: raise NotEnoughFundsException
        else: self._balance -= amount

    def getBalance(self):
        return self._balance
    
    def getOwner(self):
        return self._owner

class Bank:
    _name: str
    #Uses card number as key
    _accounts: dict[str, BankAccount]

    def __init__(self, name, accounts: dict[str, BankAccount]):
        self._name = name
        self._accounts = accounts

    def getName(self):
        return self._name
    
    def createAccount(self, owner):
        ##TODO: validation
        return BankAccount(owner)

    def getAccountBalance(self, account_id:str):
        if not isinstance(self._accounts[account_id], BankAccount):
            raise BankAccountNotFoundException
        else: return self._accounts[account_id].getBalance()

    def replenishAccount(self, account_id:str, amount:int):
        self._accounts[account_id].replenish(amount)

    def withdrawFromAccount(self, account_id:str, amount:int):
        self._accounts[account_id].withdraw(amount)

class Card:
    _emitent: str
    # card number and pin are strings because they can start with 0
    _cardNumber: str
    _bankAccountId: str
    _pin: str
    _incorrectTries: int = 0
    _blocked: bool

    def __init__(self,bank: Bank):
        #A card emitting operation. Should of course be more complicated, but it's a model after all
        self._emitent = bank.getName()
        #generate a random number
        self._cardNumber = "".join([random.choice(string.digits) for x in range(16)])
        #generate a random PIN
        self._pin = "".join([random.choice(string.digits) for x in range(4)])
        
    def unlockCard(self,pin: str):
        if self._incorrectTries > 3: raise CardIsLockedException

        validatePIN(pin)
        if self._pin == pin: return True
        else: 
            self._incorrectTries += 1
            return False



class CashVault:
    def __init__(self):
        self._availableBanknotes = dict.fromkeys(BanknoteTypes, 0)

    def addBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] += 1

    def removeBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] -= 1

    def clearVault(self):
        self._availableBanknotes = {}

    def checkAvailability(self):
        return(self._availableBanknotes)


class ATM:
    _vault: CashVault
    def __init__(self):
        self._vault = CashVault()
