import random
import string
from resources import InvalidPINException, IncorrectAmountValueException, IncorrectPhoneNumberException

def validatePIN(pin:str):
    if(len(pin) != 4): 
        raise InvalidPINException
    for char in pin:
        if char not in string.digits:
            raise InvalidPINException

def validateAmount(amount:float):
    if(amount < 0):
        raise IncorrectAmountValueException

def validatePhone(phone:str):
    if(len(phone) != 9):
        raise IncorrectPhoneNumberException 

def generatePIN() -> str:
    return "".join([random.choice(string.digits) for x in range(4)])

def generateCardNumber() -> str:
    return "".join([random.choice(string.digits) for x in range(16)])

def generateBankAccountId() -> str:
    return "".join([random.choice(string.digits) for x in range(25)])