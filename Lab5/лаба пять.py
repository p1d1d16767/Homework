from abc import ABC, abstractmethod
from functools import wraps


def log(func):
    """Декоратор, який виводить назву функції перед її викликом."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Виклик:", func.__name__)
        return func(*args, **kwargs)
    return wrapper


class Account(ABC):
    """Абстрактний базовий клас банківського рахунку."""

    def __init__(self, account_id, owner_name, balance=0):
        """Створює рахунок з ідентифікатором, власником і балансом."""
        self._id = account_id
        self._owner_name = owner_name
        self._balance = balance

    def __del__(self):
        """Повідомляє про видалення рахунку."""
        print("Рахунок", self._id, "видалено")

    @property
    def id(self):
        """Повертає ідентифікатор рахунку."""
        return self._id

    @property
    def owner_name(self):
        """Повертає ім'я власника рахунку."""
        return self._owner_name

    @property
    def balance(self):
        """Повертає поточний баланс."""
        return self._balance

    @staticmethod
    def check_amount(amount):
        """Перевіряє, що сума є додатним числом (int або float)."""
        return isinstance(amount, (int, float)) and amount > 0

    @log
    def deposit(self, amount):
        """Поповнює рахунок на вказану суму."""
        if not Account.check_amount(amount):
            print("Неправильна сума")
            return
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount):
        """Знімає кошти з рахунку (реалізується в нащадках)."""
        pass

    @abstractmethod
    def show_account(self):
        """Виводить інформацію про рахунок (реалізується в нащадках)."""
        pass


class BankAccount(Account):
    """Звичайний банківський рахунок."""

    @log
    def withdraw(self, amount):
        """Знімає кошти, якщо сума коректна і вистачає балансу."""
        if not Account.check_amount(amount):
            print("Неправильна сума")
        elif amount > self._balance:
            print("Недостатньо коштів")
        else:
            self._balance -= amount

    def show_account(self):
        """Виводить id, власника та баланс рахунку."""
        print(
            "id:", self._id,
            "| власник:", self._owner_name,
            "| баланс:", self._balance
        )


class SavingsAccount(BankAccount):
    """Накопичувальний рахунок із відсотком."""

    def __init__(self, account_id, owner_name, balance=0, percent=5):
        """Створює рахунок із заданим відсотком нарахування."""
        super().__init__(account_id, owner_name, balance)
        self._percent = percent

    def add_percent(self):
        """Нараховує відсотки на поточний баланс."""
        self._balance += self._balance * self._percent / 100

    def show_account(self):
        """Виводить інформацію про рахунок і відсоток."""
        super().show_account()
        print("відсоток:", self._percent)


class Bank:
    """Банк, що зберігає і обробляє набір рахунків."""

    def __init__(self, name):
        """Створює банк з назвою та порожнім списком рахунків."""
        self._name = name
        self._accounts = []

    def find_account(self, account_id):
        """Повертає рахунок за id або None, якщо його не знайдено."""
        for account in self._accounts:
            if account.id == account_id:
                return account
        return None

    def add_account(self, account):
        """Додає рахунок, якщо рахунку з таким id ще немає."""
        if self.find_account(account.id) is not None:
            print("Рахунок з таким id вже є")
        else:
            self._accounts.append(account)

    def remove_account(self, account_id):
        """Видаляє рахунок за id, якщо він існує."""
        account = self.find_account(account_id)
        if account is None:
            print("Рахунок не знайдено")
        else:
            self._accounts.remove(account)

    def sort_by_balance(self):
        """Сортує рахунки за зростанням балансу."""
        self._accounts.sort(key=lambda account: account.balance)

    def show_all(self):
        """Виводить назву банку та всі його рахунки."""
        print("Банк:", self._name)
        for account in self._accounts:
            account.show_account()


def main():
    """Демонструє роботу класів Account, Bank та їх нащадків."""
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


if __name__ == "__main__":
    main()
