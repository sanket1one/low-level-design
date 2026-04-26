"""
POLYMORPHISM:

The ability of an object to take many forms.

In Python, polymorphism is achieved through method overriding and method overloading.

same method on different object can have different behavior.

loose coupling

compile-time: method overloading (not supported in Python)
run-time: method overriding (supported in Python)
"""

# Compile-time polymorphism: (method overloading)
class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(2, 3)) # 5
print(calc.add(2, 3, 4)) # 9
print(calc.add(2.4, 3.6)) # 6.0


# 2. Run-time polymorphism: (method overriding)
class Notification:
    def __init__(self, recipient: str, message: str):
        self._recipient = recipient
        self._message = message

    def send(self):
        print(f"Sending generic notification to {self._recipient}")


class EmailNotification(Notification):
    def __init__(self, recipient: str, message: str, subject: str):
        super().__init__(recipient, message)
        self._subject = subject

    def send(self):
        print(f"Sending EMAIL to {self._recipient} | Subject: {self._subject}")


class SMSNotification(Notification):
    def __init__(self, recipient: str, message: str, phone_number: str):
        super().__init__(recipient, message)
        self._phone_number = phone_number

    def send(self):
        print(f"Sending SMS to {self._phone_number} | Message: {self._message}")