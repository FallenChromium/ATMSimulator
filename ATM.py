from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from Bank import Bank, Card
from interface.MainMenu import MainMenu
from interface.PINDialogue import PINDialogue
from resources import BanknoteTypes
import settings


class CashVault:
    def __init__(self, availableBanknotes: dict[int, int] = dict.fromkeys(BanknoteTypes, 0)):
        self._availableBanknotes = availableBanknotes

    def addBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] += 1

    def removeBanknote(self, banknote: BanknoteTypes):
        self._availableBanknotes[banknote] -= 1

    def clearVault(self):
        self._availableBanknotes = {}

    def checkAvailability(self):
        return(self._availableBanknotes)


class ATM:
    _card: Card
    _vault: CashVault
    bank: Bank
    accountId: str

    def __init__(self, cash_vault: CashVault = CashVault()):
        self._vault = cash_vault

    def start(self, cards):
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Button", style="dim")
        table.add_column("Number", style="dim")
        for idx, card in enumerate(cards):
            table.add_row(str(idx), card._cardNumber)
        console.print(table)
        choice = int(
            Prompt.ask(
                "Which card will you insert?",
                choices=[str(x) for x in range(0, len(cards))]
            )
        )
        self._card = cards[choice]
        bankname = self._card._emitent
        self.accountId = self._card.getBankAccountId()
        self.bank = next(
            (bank for bank in settings.banks if bank.name == bankname))
        PINDialogue()
    
    def calculateWithdraw(self, amount: int) -> int:
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

    def withdraw(self, amount: int):
        can_give = 0
            #for each banknote nominal, starting from the biggest
        for i in sorted(self._vault.checkAvailability().keys(), reverse=True):
            while (self._vault.checkAvailability()[i] > 0):
                if (can_give + i <= amount):
                    self._vault.removeBanknote(BanknoteTypes(i))
                    can_give += i
                    print(BanknoteTypes(i))
                else: break
