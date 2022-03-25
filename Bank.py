from resources import NotEnoughFundsException, CardIsLockedException, BankAccountNotFoundException
from utilities import generateBankAccountId, generateCardNumber, generatePIN, validateAmount, validatePIN


class BankAccount:
    _balance: int = 0
    _owner: str = ""
    _id: str

    def __init__(self, owner, balance: int = 0, id: str = generateBankAccountId()):
        self._balance: int = balance
        self._owner: str = owner
        self._id: str = id

    def replenish(self, amount):
        validateAmount(amount)
        self._balance += amount

    def withdraw(self, amount):
        validateAmount(amount)
        if self._balance - amount < 0:
            raise NotEnoughFundsException
        else:
            self._balance -= amount

    def getBalance(self):
        return self._balance

    def getOwner(self):
        return self._owner


class Card:
    _emitent: str
    # card number and pin are strings because they can start with 0
    _cardNumber: str
    __bankAccountId: str
    __pin: str
    __incorrectTries: int = 0
    _blocked: bool

    def __init__(self, bankname: str, bankAccountId: str, cardNumber: str = generateCardNumber(), pin: str = generatePIN()):
        # A card emitting operation. Should of course be more complicated, but it's a model after all
        self._emitent = bankname
        # generate a random number
        self._cardNumber = cardNumber
        # generate a random PIN
        self.__pin = pin
        # Generate a random bank account ID
        self.__bankAccountId = bankAccountId

    def getBankAccountId(self):
        return self.__bankAccountId

    def unlockCard(self, pin: str):
        if self.__incorrectTries > 3:
            raise CardIsLockedException
        if self.__pin == pin:
            return True
        else:
            self.__incorrectTries += 1
            return False


class Bank:
    _name: str
    # Uses card number as key
    _accounts: dict[str, BankAccount]
    _cards: dict[str, Card]

    def __init__(self, name, accounts: dict[str, BankAccount]):
        self._name = name
        self._accounts = accounts

    def getName(self):
        return self._name

    def createAccount(self, owner):
        ##TODO: validation
        return BankAccount(owner)

    def getAccountBalance(self, account_id: str):
        if not isinstance(self._accounts[account_id], BankAccount):
            raise BankAccountNotFoundException
        else:
            return self._accounts[account_id].getBalance()

    def replenishAccount(self, account_id: str, amount: int):
        self._accounts[account_id].replenish(amount)

    def withdrawFromAccount(self, account_id: str, amount: int):
        self._accounts[account_id].withdraw(amount)
