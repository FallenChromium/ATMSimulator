from model.Bank import Card
from resources import BanknoteTypes
from typing import Union
from resources import BankIsUnsupportedException
import settings


class CashVault:
    def __init__(self, availableBanknotes: dict[int, int] = dict.fromkeys(BanknoteTypes, 0)):
        self._availableBanknotes = availableBanknotes

    def __serialize__(self):
        return self._availableBanknotes

    def addBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] += 1

    def removeBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] -= 1

    def clearVault(self):
        self._availableBanknotes = {}

    def checkAvailability(self):
        return(self._availableBanknotes.copy())


class ATM:
    _card: Union[Card, None]
    _vault: CashVault

    def __serialize__(self):
        return {'cash_vault': self._vault, 'bankname': self._bankname, 'accountId': self._accountId}


    def __init__(self, cash_vault: CashVault, bankname: Union[str, None] = None, accountId: Union[str, None] = None):
        self._vault = cash_vault
        self._bankname = bankname
        self._accountId = accountId

    def authenticate(self, card_index):
        card = settings.cards[card_index]
        self._bankname = card._emitent
        self._accountId = card.getBankAccountId()

    def logout(self):
        self._bankname = None
        self._accountId = None
    
    def calculateWithdraw(self, amount: float) -> float:
        can_give = 0
        available = self._vault.checkAvailability()
            #for each banknote nominal, starting from the biggest
        for i in sorted(available.keys(), reverse=True):
            while (available[i] > 0):
                if (can_give + i <= amount):
                    available[i] -= 1
                    can_give += i
                else: break

        return can_give

    def getBank(self):
        bank = next((bank for bank in settings.banks if bank.name == self._bankname), None) 
        if bank is not None:
            return bank
        else: raise(BankIsUnsupportedException)
    
    def getAccountId(self):
        return self._accountId

    # call this only after verifying that the money is successfully subtracted from the account!
    def withdraw(self, amount: float) -> list[str]:
        can_give = 0
        cash = []
            #for each banknote nominal, starting from the biggest
        for i in sorted(self._vault.checkAvailability().keys(), reverse=True):
            while (self._vault.checkAvailability()[i] > 0):
                if (can_give + i <= amount):
                    self._vault.removeBanknote(BanknoteTypes(i))
                    can_give += i
                    cash.append(BanknoteTypes(i))
                else: break
        return cash
    
    def isCardInserted(self):
        return self._accountId is not None
