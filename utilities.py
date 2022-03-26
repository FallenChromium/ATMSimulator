import random
import string
from resources import IncorrectPINException, IncorrectAmountValueException, IncorrectPhoneNumberException

def validatePIN(pin:str):
    if(len(pin) != 4): 
        raise IncorrectPINException
    for char in pin:
        if char not in string.digits:
            raise IncorrectPINException

def validateAmount(amount:int):
    if(amount < 0 or not isinstance(amount, int)):
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