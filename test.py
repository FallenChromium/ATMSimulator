import unittest
from ATM import CashVault
from Bank import Bank, BankAccount
from resources import BanknoteTypes, NotEnoughFundsException


class TestCashVault(unittest.TestCase):

    def test_insertion(self):
        self.vault = CashVault()

        # Add several banknotes
        self.vault.addBanknote(BanknoteTypes.BYN10)
        self.vault.addBanknote(BanknoteTypes.BYN20)

        # Check if they do exist in the vault in the correct quantity
        self.assertTrue(self.vault.checkAvailability()
                        [BanknoteTypes.BYN10] == 1)
        self.assertTrue(self.vault.checkAvailability()
                        [BanknoteTypes.BYN20] == 1)

        # Check that by default vault does not contain banknotes
        self.assertTrue(self.vault.checkAvailability()[
                        BanknoteTypes.BYN200] == 0)

    def test_removal(self):
        self.vault2 = CashVault()

        # Add 3 banknotes of the same type
        self.vault2.addBanknote(BanknoteTypes.BYN10)
        self.vault2.addBanknote(BanknoteTypes.BYN10)
        self.vault2.addBanknote(BanknoteTypes.BYN10)

        # Check that after removal only 2 banknotes are left
        self.vault2.removeBanknote(BanknoteTypes.BYN10)
        self.assertTrue(self.vault2.checkAvailability()
                        [BanknoteTypes.BYN10] == 2)


class TestBank(unittest.TestCase):
    def testInit(self):
        # It is passed to bank constructor rather than being created with createAccount for serialization check and further checkBalance function test
        accounts: dict[str, BankAccount] = {
            "bankaccount1": BankAccount("John Doe"),
            "bankaccount2": BankAccount("Alice Caroll"),
            "bankaccount3": BankAccount("Bob Marley")
        }

        self.bank = Bank("CapitalistHive L.L.C.", accounts)
        self.assertTrue(self.bank.getName() == "CapitalistHive L.L.C.")
        # Should be zero, because we've just created the account and didn't replenish it
        self.assertTrue(
            # get ID of a first account in a dict
            self.bank.getAccountBalance(list(accounts.keys())[0]) == 0
        )

    def testReplenish(self):
        self.accounts: dict[str, BankAccount] = {
            "bankaccount1": BankAccount("John Doe")
        }

        self.bank = Bank("CapitalistHive L.L.C.", self.accounts) 
        accountId: str = list(self.accounts.keys())[0] 
        #should throw NotEnoughFunds
        with self.assertRaises(NotEnoughFundsException):
            self.bank.withdrawFromAccount(accountId, 300)
        
    def testWithdraw(self):
        self.accounts: dict[str, BankAccount] = {
            "bankaccount1": BankAccount("John Doe")
        }

        self.bank = Bank("CapitalistHive L.L.C.", self.accounts) 
        accountId: str = list(self.accounts.keys())[0]  
        self.bank.replenishAccount(accountId, 300)
        self.assertTrue(self.bank.getAccountBalance(accountId) == 300)

if __name__ == '__main__':
    unittest.main()
