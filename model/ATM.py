from model.Bank import Card
from resources import BanknoteTypes
from typing import Union
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
        return {'cash_vault': self._vault, 'card': self._card}


    def __init__(self, cash_vault: CashVault, card):
        self._vault = cash_vault
        self._card = card

    def authenticate(self, card_index):
        self._card = settings.cards[card_index]
        bankname = self._card._emitent
        self.bank = next(
            (bank for bank in settings.banks if bank.name == bankname))

    def logout(self):
        self._card = None
    
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
        return next(bank for bank in settings.banks if bank.name == self._card._emitent)
    
    def getAccountId(self):
        return self._card.getBankAccountId()

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
        return self._card is not None

        return cash
