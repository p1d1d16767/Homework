from abc import ABC, abstractmethod


def log(func):
    def wrapper(*args, **kwargs):
        print("Виклик:", func.__name__)
        return func(*args, **kwargs)
    return wrapper


class Account(ABC):
    def __init__(self, id, owner_name, balance=0):
        self._id = id
        self._owner_name = owner_name
        self._balance = balance

    def __del__(self):
        print("Рахунок", self._id, "видалено")

    @property
    def id(self):
        return self._id

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def balance(self):
        return self._balance

    @staticmethod
    def check_amount(amount):
        return (type(amount) == int or type(amount) == float) and amount > 0

    @log
    def deposit(self, amount):
        if not Account.check_amount(amount):
            print("Неправильна сума")
            return
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def showAccount(self):
        pass


class BankAccount(Account):
    @log
    def withdraw(self, amount):
        if not Account.check_amount(amount):
            print("Неправильна сума")
        elif amount > self._balance:
            print("Недостатньо коштів")
        else:
            self._balance -= amount

    def showAccount(self):
        print("id:", self._id, "| власник:", self._owner_name, "| баланс:", self._balance)


class SavingsAccount(BankAccount):
    def __init__(self, id, owner_name, balance=0, percent=5):
        super().__init__(id, owner_name, balance)
        self._percent = percent

    def add_percent(self):
        self._balance += self._balance * self._percent / 100

    def showAccount(self):
        super().showAccount()
        print("відсоток:", self._percent)


class Bank:
    def __init__(self, name):
        self._name = name
        self._accounts = []

    def find_account(self, id):
        for account in self._accounts:
            if account.id == id:
                return account
        return None

    def add_account(self, account):
        if self.find_account(account.id) is not None:
            print("Рахунок з таким id вже є")
        else:
            self._accounts.append(account)

    def remove_account(self, id):
        account = self.find_account(id)
        if account is None:
            print("Рахунок не знайдено")
        else:
            self._accounts.remove(account)

    def sort_by_balance(self):
        self._accounts.sort(key=lambda account: account.balance)

    def show_all(self):
        print("Банк:", self._name)
        for account in self._accounts:
            account.showAccount()


def main():
    bank = Bank("ПриватБанк")

    a1 = BankAccount(1, "Іван", 1000)
    a2 = SavingsAccount(2, "Марія", 3000, 10)
    a3 = BankAccount(3, "Олег", 500)

    bank.add_account(a1)
    bank.add_account(a2)
    bank.add_account(a3)
    bank.add_account(BankAccount(1, "Дублікат"))
    bank.show_all()

    a1.deposit(200)
    a1.deposit(50.5)
    a1.deposit(-5)
    a1.withdraw(300)
    a1.withdraw(5000)

    a2.add_percent()

    bank.sort_by_balance()
    bank.show_all()

    bank.remove_account(3)
    bank.remove_account(10)
    bank.show_all()


main()