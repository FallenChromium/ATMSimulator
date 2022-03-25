from Bank import Card
from rich.prompt import Prompt

from interface.BaseMenu import BaseMenu
from interface.ShowBalanceMenu import showBalanceMenu
from interface.PhoneRefillMenu import phoneRefillMenu
from interface.WithdrawalMenu import withdrawalMenu


class MainMenu(BaseMenu):
    def __init__(self):
        BaseMenu.__init__(self, actionlist={
            "1": (showBalanceMenu.show, "Check balance"),
            "2": (withdrawalMenu.show, "Withdraw from account"),
            "3": (phoneRefillMenu.show, "Top up your phone balance"),
            "0": (exit, "Exit")
        })
    
    def show(self):
        while True:
            super().show()
