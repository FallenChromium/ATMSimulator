from abc import ABC, abstractmethod
 
class IView(ABC):
 
    def __init__(self, controller):
        self.controller = controller
        super().__init__()
    
    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def show_available_cards(self, cards):
        pass

    @abstractmethod
    def phone_topup(self):
        pass

    @abstractmethod
    def withdraw(self):
        pass
    @abstractmethod
    def show_balance(self):
        pass