from atexit import register
import json
from ATM import ATM, CashVault
from Bank import Bank, BankAccount, Card
from resources import ReadError
import settings


@register
def termin():
    print(" Goodbye!")


def import_data():
    try:
        file = open(settings.backupPath, "r")
    except IOError:
        raise(Exception("Database doesn't exist"))
    else:
        with file as jsonPayload:
            data = json.load(jsonPayload)
        try:
            # Parse JSON into an object with attributes corresponding to dict keys.
            # Reference: https://pynative.com/python-convert-json-data-into-custom-python-object/
            print(data)
            settings.banks = loadBanks(data)
            settings.cards = loadCards(data)
            settings.atm = loadATM(data)
        except KeyError as exception:
            print("Incorrect database")
            raise(exception)
        except ValueError as exception:
            print("Incorrect database")
            raise(exception)


def loadAccounts(obj) -> dict[str, BankAccount]:
    accounts: dict[str, BankAccount] = {}
    if 'accounts' in obj:
        for account in obj['accounts']:
            accounts[str(account["id"])] = BankAccount(
                account["owner"], account["balance"], account["id"])
        return accounts
    else:
        raise(ReadError)


def loadBanks(obj):
    print(obj)
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
            {int(key): value for key, value in obj['ATM']["cash_vault"].items()})
        atm: ATM = ATM(cash_vault)
        return atm
    else:
        raise(ReadError)


if __name__ == "__main__":
    import_data()
    settings.atm.start(settings.cards)
