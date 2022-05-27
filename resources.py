import enum

class IncorrectPINException(Exception):

    def __str__(self):
        return "Incorrect PIN. Valid PIN: 4 digits"


class CardAlreadyInsertedException(Exception):

    def __str__(self):
        return "Card already inserted"


class BankAccountNotFoundException(Exception):

    def __str__(self):
        return "Bank account cannot be found"


class IncorrectAmountValueException(Exception):

    def __str__(self):
        return "Nope. You can't use THAT as money amount"

class IncorrectPhoneNumberException(Exception):

    def __str__(self):
        return "Your phone number is incorrect. Try again!"

class NotEnoughFundsException(Exception):

    def __str__(self):
        # this is a Starcraft reference
        return "Not enough minerals"


class CardIsLockedException(Exception):

    def __str__(self):
        # this is a Starcraft reference
        return "Sorry, your card is locked. Visit the nearest bank office for assistance!"

class AuthenticationRequiredException(Exception):

    def __str__(self):
        # this is a Starcraft reference
        return "Sorry, but you didn't log in. This operation requires you to authenticate!"

class BankIsUnsupportedException(Exception):

    def __str__(self):
        return "We are not connected to this bank's database. Please try a different ATM."


class ReadError(Exception):
    def __str__(self):
        return "Database is incorrect."


class BanknoteTypes(enum.IntEnum):
    BYN5 = 5
    BYN10 = 10
    BYN20 = 20
    BYN50 = 50
    BYN100 = 100
    BYN200 = 200
