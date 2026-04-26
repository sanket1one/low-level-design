"""
Composition:

Strong relationship.

part is meaningless with the whole.

Has-a relationship.


“This object is composed of other objects.”
“And if the container goes away, so do its parts.”

House and Rooms:

<.>---

car 1<.>----1 Engine
car 1<.>----* Doors.

"""

class LineItem:
    def __init__(self, product_name, quantity, unit_price):
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_subtotal(self):
        return self.quantity * self.unit_price

    def describe(self):
        print(f"{self.product_name} x{self.quantity} "
              f"@ ${self.unit_price:.2f} = ${self.get_subtotal():.2f}")

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.line_items = []

    def add_item(self, product, quantity, unit_price):
        self.line_items.append(LineItem(product, quantity, unit_price))

    def remove_item(self, product):
        self.line_items = [
            item for item in self.line_items
            if item.product_name != product
        ]

    def get_total(self):
        return sum(item.get_subtotal() for item in self.line_items)

    def print_receipt(self):
        print(f"Order: {self.order_id}")
        for item in self.line_items:
            item.describe()
        print(f"Total: ${self.get_total():.2f}")

if __name__ == "__main__":
    order = Order("ORD-1001")
    order.add_item("Wireless Mouse", 2, 29.99)
    order.add_item("USB-C Cable", 3, 9.99)
    order.add_item("Laptop Stand", 1, 49.99)

    order.print_receipt()

    # When order is deleted, all LineItems are destroyed with it.
    # No LineItem exists outside of an Order.