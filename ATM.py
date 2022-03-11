from resources import BanknoteTypes



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
