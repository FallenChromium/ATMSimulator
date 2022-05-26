from atexit import register
from controller.controller import ATMController
from model.storage_json import import_data, export_data

@register
def termin():
    export_data(atm)


if __name__ == "__main__":
    # initialize model (also populates global settings.py with cards and banks)
    try:
        atm = import_data()
    except Exception as e:
        print(e)
        exit(1)
        
    # initialize controller
    controller = ATMController(atm)
    controller.startUI("cli")
    
