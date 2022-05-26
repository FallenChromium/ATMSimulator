from resources import NotEnoughFundsException, CardIsLockedException, BankAccountNotFoundException
from utilities import generateBankAccountId, generateCardNumber, generatePIN, validateAmount 


class BankAccount:
    __balance: float = 0
    __owner: str = ""
    __id: str

    def __init__(self, owner, balance: float = 0, id: str = generateBankAccountId()):
        self.__balance: float = balance
        self.__owner: str = owner
        self.__id: str = id

    def __serialize__(self):
        return {"owner": self.__owner, "id": self.__id, "balance": self.__balance}

    def replenish(self, amount):
        validateAmount(amount)
        self.__balance += amount

    def withdraw(self, amount):
        validateAmount(amount)
        if self.__balance - amount < 0:
            raise NotEnoughFundsException
        else:
            self.__balance -= amount

    def getBalance(self):
        return self.__balance

    def getOwner(self):
        return self.__owner
    
    def getId(self):
        return self.__id


class Card:
    _emitent: str
    # card number and pin are strings because they can start with 0
    _cardNumber: str
    __bankAccountId: str
    __pin: str
    __incorrectTries: int = 0
    _blocked: bool

    def __init__(self, emitent: str, bankAccountId: str, cardNumber: str = generateCardNumber(), pin: str = generatePIN(), incorrectTries: int = 0, blocked: bool = False):
        # A card emitting operation. Should of course be more complicated, but it's a model after all
        self._emitent = emitent
        # generate a random number
        self._cardNumber = cardNumber
        # generate a random PIN
        self.__pin = pin
        # Generate a random bank account ID
        self.__bankAccountId = bankAccountId
        
        self.__incorrectTries = incorrectTries
        self._blocked = blocked

    def __serialize__(self):
        return {"emitent": self._emitent, "bankAccountId": self.__bankAccountId, "cardNumber": self._cardNumber, "pin": self.__pin, "incorrectTries": self.__incorrectTries, "blocked": self._blocked}

    def getBankAccountId(self):        
        return self.__bankAccountId

    def unlockCard(self, pin: str):
        if self._blocked == True:
            raise CardIsLockedException
        if self.__pin == pin:
            self.__incorrectTries = 0
            return True
        else:
            self.__incorrectTries += 1
            if self.__incorrectTries >= 3:
                self._blocked = True
            return False


class Bank:
    name: str
    # Uses bankAccountId as key (emulates database indexing behavior)
    __accounts: dict[str, BankAccount]

    def __init__(self, name, accounts: list[BankAccount]):
        self.name = name
        self.__accounts = {account.getId(): account for account in accounts}

    def __serialize__(self):
        return {"name": self.name, "accounts": list(self.__accounts.values())}

    def getName(self):
        return self.name

    def createAccount(self, owner):
        ##TODO: validation
        return BankAccount(owner)

    def getAccountBalance(self, account_id: str) -> float:
        if not isinstance(self.__accounts[account_id], BankAccount):
            raise BankAccountNotFoundException
        else:
            return self.__accounts[account_id].getBalance()

    def replenishAccount(self, account_id: str, amount: int):
        self.__accounts[account_id].replenish(amount)

    def withdrawFromAccount(self, account_id: str, amount: float):
        self.__accounts[account_id].withdraw(amount)
