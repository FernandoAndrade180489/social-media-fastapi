import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds


# Fixture - Function that run before test case
@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

    
def test_subtract():
    assert subtract(9, 4) == 5

    
def test_multiply():
    assert multiply(4 ,3) == 12

    
def test_divide():
    assert divide(10, 2) == 5   


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50
    
def test_bank_defaut_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposite(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])    
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


# To Test raise exception expected
def test_insufficients_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)
        
# To Test raise exception expected
# Type of exception is important, this case works because InsufficientFunds is extend by Exception class - class InsufficientFunds(Exception)
def test_insufficients_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
    
    