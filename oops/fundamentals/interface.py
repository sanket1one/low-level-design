"""
Interface:

-> well defined contract between two entities
-> loosely coupled.


Example:
    Remote[FEATURE]:
        -> play()
        -> puase()
        -> volumeUp()
        -> volumeDown()

    control tv, soundbar, projector. [perform same action]


    [
        <<interface>> RemoteControl ||
        + play () : void
        + pause () : void
        + volumeUp () : void
        + volumeDown () : void
    ]
    
    <<RemoteControl>> -> [
        TV || 
        + play ()
        + pause () 
        + volumeUp ()
        + volumeDown ()
    ]
    <<RemoteControl>>    -> [Soundbar || 
        + play ()
        + pause ()
        + volumeUp () 
        + volumeDown ()
    ]
    <<RemoteControl>>    -> [Projector || 
        + play ()
        + pause ()
        + volumeUp ()
        + volumeDown ()
    ]

    - encapsulation
    - polymorphism
    - Decoupling
}
"""

"""
Notification service:

"""
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotifer(NotificationService):
    def send(self, message):
        print(f"Sending email with message: {message}")

class WebhookNotifier(NotificationService):
    def send(self, message):
        print(f"Sending webhook with message: {message}")

class SlackNotifier(NotificationService):
    def send(self, message):
        print(f"Sending slack message: {message}")

class AlterService:
    def __init__(self, notfier: NotificationService):
        self._notifier = notfier

    def trigger_alter(self, message):
        alter_message = f"ALERT: {message}"
        self._notifier.send(alter_message)


print("**--------------------EX:1 Log Formatter --------------------**")

"""
Design Log Formatter Class
Problem: Build a logging system where the format of log messages is configurable. A Logger class writes log messages, but the format (plain text vs. JSON) is determined by an injected Formatter interface.

Requirements:

Formatter interface with a format(message) method that takes a string and returns a formatted string
PlainFormatter: returns the message as-is (e.g., "Server started on port 8080")
JsonFormatter: returns the message wrapped in JSON (e.g., {"log": "Server started on port 8080"})
Logger class takes a Formatter in its constructor and has a log(message) method that formats the message, then prints it

"""


class Formatter(ABC):
    @abstractmethod
    def format(self, message: str) -> str:
        pass

class PlainFormatter(Formatter):
    def format(self, message: str) -> str:
        return message


class JsonFormatter(Formatter):
    def format(self, message: str) -> str:
        return f'{{"log": "{message}"}}'

class Logger:
    def __init__(self, formatter: Formatter):
        self._formatter = formatter
    
    def log(self, message: str) -> str:
        formatted_message = self._formatter.format(message)
        print(formatted_message)

plain_logger = Logger(PlainFormatter())
plain_logger.log("Server started on port 8080")

json_logger = Logger(JsonFormatter())
json_logger.log("Server started on port 8080")


print("**--------------------EX:2 Input Validator --------------------**")

"""
Design Input Validator Class
Problem: Build a registration system where multiple validation rules are applied to user input. Each rule is a separate implementation of a Validator interface, and the RegistrationService runs all validators before accepting the registration.

Requirements:

Validator interface with a validate(input) method that returns true if valid, false otherwise
EmailValidator: returns true if the input contains @
PasswordValidator: returns true if the input has 8 or more characters
RegistrationService: takes a list of validators in its constructor. Its register(input) method runs all validators and prints whether the input passed or failed
"""
class Validator(ABC):
    @abstractmethod
    def validate(self, input: str) -> bool:
        pass

class EmailValidator(Validator):
    def validate(self, input: str) -> bool:
        return "@" in input

class PasswordValidator(Validator):
    def validate(self, input: str) -> bool:
        return len(input) >= 8
    
class RegistrationService:
    def __init__(self, validators: list[Validator]):
        self._validators = validators
    

    def register(self, input: str):
        for validator in self._validators:
            if not validator.validate(input):
                print(f" {input} - FAILED.")
            else:
                print(f" {input} - PASSED.")


email_reg = RegistrationService([EmailValidator()])
email_reg.register("user@example.com")  # Should pass
email_reg.register("invalid-email")      # Should fail

pass_reg = RegistrationService([PasswordValidator()])
pass_reg.register("strongpassword")  # Should pass
pass_reg.register("short")            # Should fail