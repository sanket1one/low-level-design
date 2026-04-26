"""
Dependency:

one class relies on another to fulfil it's responsibility.

Imagine a Chef preparing a meal.

The chef picks up a Knife to chop vegetables.
Once the chopping is done, the knife is put away or reused elsewhere.
The chef doesn’t necessarily own the knife or keep it stored long-term.


UML --->  dashed arrow

Printer ---> documents

printer uses docuements  during it's print() method but doesn't sotre it as a field.
"""

class Document:
    def __init__(self, content):
        self.__content = content
    
    def content(self):
        return self.__content

class Printer:
    def print(doc: Document):
        print("Printing: ", doc.content)


## Exmaple:

class NotificationService:
    def __init__(self):
        self.sender = EmailSender()  # Creates its own dependency

    def notify_user(self, message):
        self.sender.send(message)



from abc import ABC, abstractmethod

class Sender(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class EmailSender(Sender):
    def send(self, message: str) -> None:
        print(f"Email: {message}")

class SmsSender(Sender):
    def send(self, message: str) -> None:
        print(f"SMS: {message}")

class NotificationService:
    def __init__(self, sender: Sender):
        self.sender = sender  # Injected from outside

    def notify_user(self, message: str) -> None:
        self.sender.send(message)


# Ticket Booking:

"""
TicketBookingService --> SeatValidtor
TicketBookingService --> PaymentProcessor
TicketBookingService --> QRCodeGenerator
TicketBookingService --> EmailService.
"""

class SeatValidator:
    def is_available(self, event_id, seat_number):
        print(f"Checking seat {seat_number} for event {event_id}")
        return True

class PaymentProcessor:
    def charge(self, email, amount):
        print(f"Charging ${amount} to {email}")
        return True  # Simulated: payment succeeds
    

class QRCodeGenerator:
    def generate(self, event_id, seat_number):
        qr_code = f"QR-{event_id}-{seat_number}"
        print(f"Generated QR code: {qr_code}")
        return qr_code

class EmailService:
    def send_confirmation(self, email, qr_code):
        print(f"Sending confirmation to {email} with code {qr_code}")


class TicketBookingService:
    def book_ticket(self, event_id, seat_number, email, amount,
                    validator, payment, qr_generator, email_service):
        if not validator.is_available(event_id, seat_number):
            print("Seat not available.")
            return False

        if not payment.charge(email, amount):
            print("Payment failed.")
            return False

        qr_code = qr_generator.generate(event_id, seat_number)
        email_service.send_confirmation(email, qr_code)

        print("Booking confirmed!")
        return True

booking_service = TicketBookingService()
validator = SeatValidator()
payment = PaymentProcessor()
qr_generator = QRCodeGenerator()
email_service = EmailService()

booking_service.book_ticket("CONF-2025", "A12", "alice@example.com",
    99.99, validator, payment, qr_generator, email_service)