import enum


class IncorrectPINException(Exception):

    def __str__(self):
        return "Incorrect PIN. Valid PIN: 4 digits"

class BankAccountNotFoundException(Exception):

    def __str__(self):
        return "Bank account cannot be found"

class IncorrectAmountValueException(Exception):

    def __str__(self):
        return "Nope. You can't use THAT as money amount"

class NotEnoughFundsException(Exception):

    def __str__(self):
        #this is a Starcraft reference
        return "Not enough minerals"

class CardIsLockedException(Exception):

    def __str__(self):
        #this is a Starcraft reference
        return "Sorry, your card is locked. Visit the nearest bank office for assistance!" 
        
class BanknoteTypes(enum.IntEnum):
    BYN5 = 5
    BYN10 = 10
    BYN20 = 20
    BYN50 = 50
    BYN100 = 100
    BYN200 = 200