import unittest
import ATM


class TestCashVault(unittest.TestCase):

    def test_insertion(self):
        self.vault = ATM.CashVault()

        # Add several banknotes
        self.vault.addBanknote(ATM.BanknoteTypes.BYN10)
        self.vault.addBanknote(ATM.BanknoteTypes.BYN20)

        # Check if they do exist in the vault in the correct quantity
        self.assertTrue(self.vault.checkAvailability()
                        [ATM.BanknoteTypes.BYN10] == 1)
        self.assertTrue(self.vault.checkAvailability()
                        [ATM.BanknoteTypes.BYN20] == 1)

        # Check that by default vault does not contain banknotes
        self.assertTrue(self.vault.checkAvailability()[
                        ATM.BanknoteTypes.BYN200] == 0)

    def test_removal(self):
        self.vault2 = ATM.CashVault()

        # Add 3 banknotes of the same type
        self.vault2.addBanknote(ATM.BanknoteTypes.BYN10)
        self.vault2.addBanknote(ATM.BanknoteTypes.BYN10)
        self.vault2.addBanknote(ATM.BanknoteTypes.BYN10)

        # Check that after removal only 2 banknotes are left
        self.vault2.removeBanknote(ATM.BanknoteTypes.BYN10)
        self.assertTrue(self.vault2.checkAvailability()
                        [ATM.BanknoteTypes.BYN10] == 2)


class TestBank(unittest.TestCase):
    def testInit(self):
        # It is passed to bank constructor rather than being created with ATM.createAccount for serialization check and further checkBalance function test
        accounts: dict[str, ATM.BankAccount] = {
            "bankaccount1": ATM.BankAccount("John Doe"),
            "bankaccount2": ATM.BankAccount("Alice Caroll"),
            "bankaccount3": ATM.BankAccount("Bob Marley")
        }

        self.bank = ATM.Bank("CapitalistHive L.L.C.", accounts)
        self.assertTrue(self.bank.getName() == "CapitalistHive L.L.C.")
        # Should be zero, because we've just created the account and didn't replenish it
        self.assertTrue(
            # get ID of a first account in a dict
            self.bank.getAccountBalance(list(accounts.keys())[0]) == 0
        )

    def testReplenish(self):
        self.accounts: dict[str, ATM.BankAccount] = {
            "bankaccount1": ATM.BankAccount("John Doe")
        }

        self.bank = ATM.Bank("CapitalistHive L.L.C.", self.accounts) 
        accountId: str = list(self.accounts.keys())[0] 
        #should throw NotEnoughFunds
        with self.assertRaises(ATM.NotEnoughFundsException):
            self.bank.withdrawFromAccount(accountId, 300)
        
    def testWithdraw(self):
        self.accounts: dict[str, ATM.BankAccount] = {
            "bankaccount1": ATM.BankAccount("John Doe")
        }

        self.bank = ATM.Bank("CapitalistHive L.L.C.", self.accounts) 
        accountId: str = list(self.accounts.keys())[0]  
        self.bank.replenishAccount(accountId, 300)
        self.assertTrue(self.bank.getAccountBalance(accountId) == 300)

if __name__ == '__main__':
    unittest.main()
