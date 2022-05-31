from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from resources import CardIsLockedException, IncorrectAmountValueException, IncorrectPINException, IncorrectPhoneNumberException, InvalidPINException, NotEnoughFundsException
import settings
from utilities import validatePhone

from view.IView import IView

class MyApp(MDApp):
    def __init__(self, widget):
        super().__init__()
        self.rootwidget = widget
    def build(self):
        return self.rootwidget

class ErrorPopup(MDDialog):
    def __init__(self, errror_text, dismiss=None): 
        super().__init__(
                text=errror_text,
                title= "Error",
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        theme_text_color="Custom",
                        on_press=self.dismiss if dismiss is None else dismiss
                    ),
                ])

class WithdrawConfirmationDialog(MDDialog):
    def __init__(self,text, amount, withdrawFunction):
        super().__init__(
            title="Confirm your actions",
            text=text,
            buttons=[
                    MDFlatButton(
                        text="RETURN",
                        theme_text_color="Custom",
                        on_press=self.dismiss
                    ),
                    MDFlatButton(
                        text="CONTINUE",
                        theme_text_color="Custom",
                        on_press=self.submit
                    )
                ],
        )
        self.withdrawFunction = withdrawFunction
        self.amount = amount

    def submit(self, button):
        self.dismiss()
        self.withdrawFunction(self.amount)


class GUIView(IView):
    def __init__(self, controller):
        super().__init__(controller)
        #initialize the UI
        self.surf = MDBoxLayout()
        self.app = MyApp(self.surf)
        self.surf.orientation = 'vertical'
        if self.controller.isCardInserted():
            self.mainMenu(None)
        else:
            self.surf.add_widget(MDLabel())
            self.surf.add_widget(MDFlatButton(text='Insert a card', on_press=self.cards))
            self.surf.add_widget(MDLabel())

    def start_atm(self):
        self.app.run()


    def logout(self, button):
        self.controller.logout()
        self.surf.clear_widgets()
        # Nobody will see it anyway, just for lulz though
        self.surf.add_widget(MDLabel(text='Have a good day!'))
        quit()

    def cards(self, button):
        self.surf.clear_widgets()
        for idx, card in enumerate(settings.cards):
            self.surf.add_widget(MDFlatButton(text=card._cardNumber, on_press=lambda _, x=idx: self.login(x)))

    def login(self, card_index):
        try:
            self.controller.loginGuard(card_index)
        except Exception as e:
            ErrorPopup(e.__str__()).open()
        else:
            # pin input that will try to authenticate later
            self.enterPin(card_index)

    def enterPin(self, card_index):
        def authenticate(card_idx, pin):
            try:
                self.controller.login(card_idx, pin)
            except IncorrectPINException as e:
                ErrorPopup(e.__str__()).open()
            except InvalidPINException as e:
                ErrorPopup(e.__str__()).open()
            except CardIsLockedException as e:
                ErrorPopup(e.__str__(), dismiss=quit).open()
            else: self.mainMenu(None)
        self.surf.clear_widgets()
        digitsPanel = Keyboard(cancel=self.logout, proceed=lambda x: authenticate(card_index,x), text="Enter PIN")
        self.surf.add_widget(digitsPanel)

    def mainMenu(self, button):
        self.surf.clear_widgets()
        self.surf.add_widget(MDFlatButton(text='View balance', on_press=self.show_balance))
        self.surf.add_widget(MDFlatButton(text='Withdraw money', on_press=self.withdraw))
        self.surf.add_widget(MDFlatButton(text='Phone payment', on_press=self.phone_topup))
        self.surf.add_widget(MDFlatButton(text='Get card', on_press=self.logout))

    def show_balance(self, button):
        self.surf.clear_widgets()
        self.surf.add_widget(MDLabel(text=str(self.controller.getBalance())))
        self.surf.add_widget(MDFlatButton(text='Back', on_press=self.mainMenu, size_hint=(1, 0.1)))

    def withdraw(self, button):
        self.surf.clear_widgets()
        self.surf.add_widget(Keyboard(proceed=lambda x: self.controller.withdrawConfirmation(x), cancel=self.mainMenu, text="Enter amount to withdraw"))

    def withdrawSummary(self, amount):
        cash = self.controller.withdraw(amount)
        self.surf.clear_widgets()
        for banknote in cash:
                self.surf.add_widget(MDLabel(text=str(banknote)))
        self.surf.add_widget(MDFlatButton(text='Back', on_press=self.mainMenu, size_hint=(1, 0.2)))

    def withdrawConfirmation(self, text: str, amount: float):
        WithdrawConfirmationDialog(text, amount, self.withdrawSummary).open()
        
        

    def phone_topup(self, button):
        self.surf.clear_widgets()
        self.surf.add_widget(Keyboard(cancel=self.mainMenu, proceed=self.inputTopupAmount, text="Enter phone number (9 numbers)"))

    def inputTopupAmount(self, phone):
        try:
            validatePhone(phone)
        except IncorrectPhoneNumberException as e:
            ErrorPopup(e.__str__()).open()
        else:
            self.surf.clear_widgets()
            self.surf.add_widget(Keyboard(proceed=lambda x: self.makePayment(phone,x), cancel = self.mainMenu, text="Enter topup amount"))

    def makePayment(self, phone, amount):
        try:
            self.controller.phoneTopup(phone, amount)
        except NotEnoughFundsException as e:
            ErrorPopup(e.__str__()).open()
        except IncorrectAmountValueException as e:
            ErrorPopup(e.__str__()).open()
        else:
            self.surf.clear_widgets()
            self.surf.add_widget(MDLabel(text='Done'))
            self.surf.add_widget(MDFlatButton(text='Back', on_press=self.mainMenu, size_hint=(1, 0.1)))


class Keyboard(MDBoxLayout):
    cancel = ObjectProperty(None)
    proceed = ObjectProperty(None)
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.name = MDLabel(text=text)
        self.label = MDLabel()
        self.grid = MDGridLayout()
        self.grid.cols = 4
        for i in range(9):
            self.grid.add_widget(MDFlatButton(text=str(i+1), on_press=self.insertSymbol))
        self.grid.add_widget(MDFlatButton(text='0', on_press=self.insertSymbol))
        self.grid.add_widget(MDFlatButton(text='Back', on_press=self.cancel))
        self.grid.add_widget(MDFlatButton(text='Enter', on_press=self.inputInfo))
        self.grid.add_widget(MDFlatButton(text='<', on_press=self.removeSymbol))
        self.grid.add_widget(MDFlatButton(text='<<<', on_press=self.removeAllSymbol))
        self.add_widget(self.name)
        self.add_widget(self.label)
        self.add_widget(self.grid)

    def insertSymbol(self, button):
        self.label.text = self.label.text + button.text

    def inputInfo(self, button):
        return self.proceed(self.label.text)

    def removeSymbol(self, button):
        self.label.text = self.label.text[:-1]

    def removeAllSymbol(self, button):
        self.label.text = ""

