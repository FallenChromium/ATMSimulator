from resources import NotEnoughFundsException, CardIsLockedException, BankAccountNotFoundException
from utilities import generateCardNumber, generatePIN, validatePIN


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
        self._cardNumber = generateCardNumber() 
        #generate a random PIN
        self._pin = generatePIN()
        
    def unlockCard(self,pin: str):
        if self._incorrectTries > 3: raise CardIsLockedException
        validatePIN(pin)
        if self._pin == pin: return True
        else: 
            self._incorrectTries += 1
            return False