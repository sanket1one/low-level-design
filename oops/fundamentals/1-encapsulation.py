"""
Encapsulation: Data hiding + Controlled access

grouping data together(variables) and behavior(methods)

it should be into one single unit(typically a class)

HOW TO ACHIEVE ENCAPSULATION IN PYTHON?

1. Access Modifies:
 -> private: __var (name mangling): Access only within the same class.
 -> protected: _var (convention): Access within the class and its subclasses. usefull when child classes need to access to parent data.
 -> public: var (default): Access from anywhere. 

"""
class BankAccount:
    def __init__(self, account_holder: str):
        self.__account_holder = account_holder
        self.__balance = 0.0
    
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount 
    
    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount
    
    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def account_holder(self):
        return self.__account_holder


myaccount = BankAccount("Sanket")
myaccount.deposit(1000)
print(myaccount.balance) # 1000.0