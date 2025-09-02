from decimal import Decimal, getcontext, localcontext, Overflow

SAFE_CTX = getcontext().copy()
SAFE_CTX.prec = 28
SAFE_CTX.Emax = 38
SAFE_CTX.Emin = -38
SAFE_CTX.traps[Overflow] = True

class Account:
    def __init__(self, balance: Decimal) -> None:
        self._balance = Decimal("0.00")

        with localcontext(SAFE_CTX):
            if balance < Decimal("0.00"):
                raise ValueError("Initial balance cannot be negative.")
            self._balance += balance

    def get_balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal) -> None:
        with localcontext(SAFE_CTX):
            if amount <= Decimal("0.00"):
                raise ValueError("Deposit amount must be positive.")
            self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal("0.00"):
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
