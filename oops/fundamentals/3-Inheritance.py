"""
INHERITANCE:

allow one class to inherit properties and behaviors from another class.

DRY
Logical hierarchy
Easy to maintenance


Type of Inheritance:
- 1. single inheritance: A child class inherits from a single parent class.
- 2. multi-level inheritance: A child class inherits from a parent class, which in turn inherits from another parent class.
- 3. multiple inheritance: A child class inherits from multiple parent classes.
"""



## Notification System Example:

from datetime import datetime


class Notification:
    def __init__(self, recipient: str, message: str):
        self._recipient = recipient
        self._message = message
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_header(self) -> str:
        return f"To: {self._recipient} | Time: {self._timestamp}"

    def send(self) -> None:
        print(self.format_header())
        print(f"Message: {self._message}")
    

class EmailNotification(Notification):
    def __init__(self, recipient: str, message: str, subject: str):
        super().__init__(recipient, message)
        self._subject = subject
    
    def format_header(self) -> str:
        base_header = super().format_header()
        return f"{base_header} | Subject: {self._subject}"
    
    def send(self) -> None:
        print(self.format_header())
        print(f"Subject: {self._subject}")
        print(f"Message: {self._message}")
        print("Email sent successfully!")

class PushNotification(Notification):
    def __init__(self, recipient: str, message: str,
                 device_token: str, priority: str):
        super().__init__(recipient, message)
        self._device_token = device_token
        self._priority = priority

    def send(self):
        print(self.format_header())
        print(f"Device: {self._device_token[:8]}...")
        print(f"Priority: {self._priority}")
        print(f"Alert: {self._message}")
        print("Status: Push notification delivered")


email = EmailNotification(
    "alice@example.com", "Your order has been shipped!", "Order Update")
email.send()

print()

push = PushNotification(
    "Charlie", "New message from Alice", "d8a3f4b2c1e5a9b7", "high")
push.send()