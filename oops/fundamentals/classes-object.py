# Classes
# Is a blueprint for creating objects. holds data and behavior.

class Car:
    total_cars = 0 # class variable

    def __init__(self, brand, radius=0): # constructor
        self.brand = brand
        self.radius = radius
        Car.total_cars += 1 # Increment total cars when a new car is created

    # can access both class and instance variables
    @classmethod
    def get_total_cars(cls):
        return cls.total_cars
    
    @staticmethod
    def is_motor_vehicle():
        return True
    
    def __str__(self):
        return f'Car(brand={self.brand})'
    

    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

try:
    c = Car("bmw", -10)
    print(c.radius)
except ValueError as e:
    print(e)
# Enums

""" Storage with fixed set of values. """
from enum import Enum

"""
Enum with properties and methods.


Coin enum: 
each coin has a name (PENNY, NICKEL, DIME, QUARTER) and a value (1, 5, 10, 25 cents).
The enum has a method to calculate the total value of a list of coins.
"""


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25

    def __init__(self, value):
        self.coin_value = value

    def get_value(self):
        return self.coin_value


total = Coin.PENNY.get_value() + Coin.NICKEL.get_value() + Coin.DIME.get_value()
print(f'Total value of coins: {total} cents')

## Practical example.
""" 
Order Processing System:

OrderStatus (which we've already seen) and PaymentMethod.Together, they demonstrate how enums bring structure and safety to a real domain model.

The Order class tracks an order's status, payment method, and total amount.
It provides methods to advance the status through its lifecycle, cancel the order, and display order information.
"""

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class PaymentMethod(Enum):
    CREDIT_CARD = ("Credit Card", 2.5)  # (name, processing fee percentage  )
    DEBIT_CARD = ("Debit Card", 1.0)
    UPI = ("UPI", 0.5)
    NET_BANKING = ("Net Banking", 1.5)

    def __init__(self, display_name: str, fee_percentage: float):
        self.display_name = display_name
        self.fee_percentage = fee_percentage

class Order:
    _status_transitions = {
        OrderStatus.PLACED: OrderStatus.CONFIRMED,
        OrderStatus.CONFIRMED: OrderStatus.SHIPPED,
        OrderStatus.SHIPPED: OrderStatus.DELIVERED,
    }


    def __init__(self, order_id: int, amount: float, payment_method: PaymentMethod):
        self._order_id = order_id
        self._status = OrderStatus.PLACED
        self._amount = amount
        self._payment_method = payment_method
    
    def advance_status(self) -> bool:
        next_status = self._status_transitions.get(self._status)
        if next_status:
            self._status = next_status
            return True
        return False

    def cancel_order(self) -> bool:
        if self._status in (OrderStatus.PLACED, OrderStatus.CONFIRMED):
            self._status = OrderStatus.CANCELED
            return True
        return False

    def get_total_with_fees(self) -> float:
        return self._amount  + (self._amount * self._payment_method.fee_percentage / 100)
    
    def display_info(self) -> None:
        print(f"Order ID: {self._order_id} | Status: {self._status.value} | Amount: ${self._amount:.2f} | Amount: ${self.get_total_with_fees():.2f} (including {self._payment_method.display_name} fees)")

    
order = Order("ORD-001",100.0, PaymentMethod.CREDIT_CARD)
order.display_info()  # Initial state


order.advance_status()  # PLACED -> CONFIRMED
# order.advance_status()  # CONFIRMED -> SHIPPED
order.display_info()  # After advancing status


print(f"Attempting to cancel order...: {order.cancel_order()}")  # Should fail since it's already SHIPPED



# practice

"""
Design Traffic Light Class
Problem: Create a TrafficLight enum where each light has a color (RED, YELLOW, GREEN), a duration in seconds, and a next() method that returns the next light in the cycle (RED -> GREEN -> YELLOW -> RED).

Requirements:

Each light has a duration property: RED = 30s, YELLOW = 5s, GREEN = 25s
next() method returns the next TrafficLight in the cycle
display() method prints the color and duration
"""

class TrafficLight(Enum):
    RED = 30
    YELLOW = 5
    GREEN = 25


    def next(self):
        if self == TrafficLight.RED:
            return TrafficLight.GREEN
        elif self == TrafficLight.GREEN:
            return TrafficLight.YELLOW
        elif self == TrafficLight.YELLOW:
            return TrafficLight.RED
    
    def display(self):
        print(f"{self.name}  {self.value}")


light = TrafficLight.RED
for _ in range(6):
    light.display()
    light = light.next()

""""
Exercise 2: HTTP Status Code


Implement HTTP Status Code
medium
Problem: Create an HttpStatus enum where each status has a numeric code and a message string.

Requirements:

Values: OK(200, "OK"), BAD_REQUEST(400, "Bad Request"), NOT_FOUND(404, "Not Found"), INTERNAL_SERVER_ERROR(500, "Internal Server Error")
isSuccess() method that returns true if the code is less than 400
display() method that prints "CODE MESSAGE" (e.g. "200 OK")
A static fromCode(int) method that returns the HttpStatus for a given code, or null/None if not found

"""


class HttpStatus(Enum):

    OK = (200, "OK")
    BAD_REQUEST = (400, "Bad Request")
    NOT_FOUND = (404, "Not Found")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")


    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
    
    def is_success(self) -> bool:
        return self.code < 400

    def display(self) -> None:
        print(f"{self.code} {self.message}")
    
    @staticmethod
    def from_code(code: int):
        for status in HttpStatus:
            if status.code == code:
                return status
        return None


HttpStatus.OK.display()
HttpStatus.NOT_FOUND.display()

print(f"Is 200 success? {str(HttpStatus.OK.is_success()).lower()}")
print(f"Is 404 success? {str(HttpStatus.NOT_FOUND.is_success()).lower()}")

found = HttpStatus.from_code(500)
if found is not None:
    print("Found by code 500: ", end="")
    found.display()