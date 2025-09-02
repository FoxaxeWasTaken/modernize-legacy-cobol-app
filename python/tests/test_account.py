import unittest
from decimal import Decimal, Overflow
from account import Account

D = Decimal

class TestAccount(unittest.TestCase):
    # --- Init ---
    def test_init_accepts_non_negative(self):
        for initial in (D("0.00"), D("100.00"), D("99.99")):
            with self.subTest(initial=initial):
                self.assertEqual(Account(balance=initial).get_balance(), initial)

    def test_init_rejects_negative(self):
        for initial in (D("-0.01"), D("-100.00")):
            with self.subTest(initial=initial):
                with self.assertRaises(ValueError):
                    Account(balance=initial)

    # --- Deposit ---
    def test_deposit_must_be_strictly_positive(self):
        acc = Account(balance=D("0.00"))

        for amt in (D("0.00"), D("-0.01")):
            with self.subTest(amt=amt):
                with self.assertRaises(ValueError):
                    acc.deposit(amt)

    def test_deposit_updates_balance(self):
        acc = Account(balance=D("0.00"))

        acc.deposit(D("99.99"))
        self.assertEqual(acc.get_balance(), D("99.99"))

    # --- Withdraw ---
    def test_withdraw_must_be_strictly_positive(self):
        acc = Account(balance=D("100.00"))

        for amt in (D("0.00"), D("-1.00")):
            with self.subTest(amt=amt):
                with self.assertRaises(ValueError):
                    acc.withdraw(amt)

    def test_withdraw_updates_balance(self):
        acc = Account(balance=D("100.00"))

        acc.withdraw(D("0.01"))
        self.assertEqual(acc.get_balance(), D("99.99"))

    def test_withdraw_equal_to_balance_allowed(self):
        acc = Account(balance=D("50.00"))

        acc.withdraw(D("50.00"))
        self.assertEqual(acc.get_balance(), D("0.00"))

    def test_withdraw_exceeding_balance_raises(self):
        acc = Account(balance=D("50.00"))

        with self.assertRaises(ValueError):
            acc.withdraw(D("50.01"))

    # --- Get Balance ---
    def test_get_balance(self):
        acc = Account(balance=D("100.00"))

        self.assertEqual(acc.get_balance(), D("100.00"))

    # --- Overflow ---

    def test_deposit_overflow(self):
        acc = Account(balance=D("0.00"))

        with self.assertRaises(Overflow):
            acc.deposit(D("1.00E+40"))

    def test_init_overflow(self):
        with self.assertRaises(Overflow):
            Account(balance=D("1.00E+40"))

if __name__ == "__main__":
    unittest.main()
