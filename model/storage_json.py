from model.ATM import ATM, CashVault
from model.Bank import Bank, BankAccount, Card
from resources import ReadError
import settings
import json


class ATMEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__dict__()` method,
    if available, to obtain its default JSON representation. 
    """

    def default(self, obj):
        if hasattr(obj, '__serialize__'):
            return obj.__serialize__()
        return json.JSONEncoder.default(self, obj)


def export_data(atm: ATM, filepath: str = ""):
    with open(settings.backupPath if filepath == "" else filepath, "w") as dataFile:
        json.dump({"banks": settings.banks, "cards": settings.cards,
                  "ATM": atm}, dataFile, cls=ATMEncoder, indent=4)


def import_data(filepath: str = "") -> ATM:
    try:
        file = open(settings.backupPath if filepath == "" else filepath, "r")
    except IOError:
        raise(Exception("Database doesn't exist"))
    else:
        with file as jsonPayload:
            data = json.load(jsonPayload)
        try:
            # Parse JSON into an object with attributes corresponding to dict keys.
            # Reference: https://pynative.com/python-convert-json-data-into-custom-python-object/
            settings.banks = loadBanks(data)
            settings.cards = loadCards(data)
            return loadATM(data)
        except Exception as e:
            raise ReadError

''' 
The reasoning behind creating functions to import data in a separate file, while exporting inside classes:
Import is happening from a specific structure (JSON, in this specific case)
Functions inside classes (__serialize__) export into a generic structure using default python types, 
which are then processed by a saving function (ATMDecoder in this case)
This architecture allows adding new file formats and storage backends easily
'''

def loadAccounts(obj) -> list[BankAccount]:
    accounts: list[BankAccount] = []
    if 'accounts' in obj:
        for account in obj['accounts']:
            accounts.append(BankAccount(
                account["owner"], account["balance"], account["id"])
            )
        return accounts
    else:
        raise(ReadError)


def loadBanks(obj):
    banks: list[Bank] = []
    if 'banks' in obj:
        for bank in obj['banks']:
            banks.append(Bank(bank['name'], loadAccounts(bank)))
        return banks
    else:
        raise(ReadError)


def loadCards(obj):
    cards: list[Card] = []
    if 'cards' in obj:
        for card in obj['cards']:
            cards.append(Card(card['emitent'], card['bankAccountId'], card['cardNumber'],
                         card['pin'], card['incorrectTries'], card['blocked']))
        return cards
    else:
        raise(ReadError)


def loadATM(obj):
    if 'ATM' in obj:
        cash_vault = CashVault(
            {int(key): value for key, value in obj['ATM']["cash_vault"].items()}
        )
        card = obj['ATM']["card"]
        card_obj = Card(card['emitent'], card['bankAccountId'], card['cardNumber'],
                         card['pin'], card['incorrectTries'], card['blocked']) if card is not None else None

        atm: ATM = ATM(cash_vault, card_obj)
        return atm
    else:
        raise(ReadError)
