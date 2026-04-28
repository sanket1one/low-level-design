"""

                 +----------------+
                 |     Client     |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 |  Application   |
                 +-------+--------+
                         |
                         v
                 +----------------------+
                 | NotificationFactory  |
                 +-----------+----------+
                             |
           +-----------------+-----------------+
           |                                   |
           v                                   v
   +----------------+                 +----------------+
   |  EmailFactory  |                 |   SmsFactory   |
   +-------+--------+                 +-------+--------+
           |                                   |
           |                                   |
   +-------+-------+                   +-------+-------+
   |               |                   |               |
   v               v                   v               v
+--------+     +--------+         +--------+     +--------+
| Message|     | Sender |         | Message|     | Sender |
+----+---+     +---+----+         +----+---+     +---+----+
     |             |                  |             |
     v             v                  v             v
+-----------+ +-----------+      +-----------+ +-----------+
|EmailMessage| |EmailSender|      |SmsMessage | |SmsSender |
+-----------+ +-----------+      +-----------+ +-----------+
"""
from abc import ABC, abstractmethod

class Message(ABC):
    @abstractmethod
    def set_content(self, to: str, body:str):
        pass

    @abstractmethod
    def format(self) -> str:
        pass

class Sender(ABC):
    @abstractmethod
    def send(self, message: Message):
        pass

#Email
class EmailMessage(Message):
    def set_content(self, to: str, body: str):
        self.to = to
        self.body = body

    def format(self) -> str:
        return f"Email to <{self.to}>: {self.body}"

class EmailSender(Sender):
    def send(self, message: Message):
        print(f"Sending via SMTP: {message.format()}")


# SMS Products
class SmsMessage(Message):
    def set_content(self, to: str, body: str):
        self.to = to
        self.body = body[:160]

    def format(self) -> str:
        return f"SMS to {self.to}: {self.body}"

class SmsSender(Sender):
    def send(self, message: Message):
        print(f"Sending via carrier API: {message.format()}")

class NotificationFactory(ABC):
    @abstractmethod
    def create_message(self) -> Message:
        pass
        
    @abstractmethod
    def create_sender(self) -> Sender:
        pass


# Email
class EmailFactory(NotificationFactory):
    def create_message(self) -> Message:
        return EmailMessage()
    
    def create_sender(self) -> Sender:
        return EmailSender()

class SmsFactory(NotificationFactory):
    def create_message(self) -> Message:
        return SmsMessage()

    def create_sender(self) -> Sender:
        return SmsSender()


class NotificationService:
    def __init__(self, factory: NotificationFactory):
        self.factory = factory
    
    def notify(self, to: str, body: str):
        message = self.factory.create_message()
        message.set_content(to, body)
        sender = self.factory.create_sender()
        sender.send(message)


print("=== Email Notification ===")
email_service = NotificationService(EmailFactory())
email_service.notify("sanketpatil8234@gmail.com", "you have applied to the job")

print()

sms_service = NotificationService(SmsFactory())
sms_service.notify("+1-555-0123", "Your order has been shipped!")

# Building UI Framework:
"""
Theme : Dark and light
ThemeColor
ThemeFont

"""
from abc import ABC, abstractmethod

class ThemeColor(ABC):
    @abstractmethod
    def apply(self):
        pass

class ThemeFont(ABC):
    @abstractmethod
    def render(self):
        pass

class LightColor(ThemeColor):
    def apply(self):
        print("Applying light color: #FFFFFF background, #000000 text")


class DarkColor(ThemeColor):
    def apply(self):
        print("Applying dark color: #1E1E1E background, #FFFFFF text")


class LightFont(ThemeFont):
    def render(self):
        print("Rendering light theme font: Arial, 14px")


class DarkFont(ThemeFont):
    def render(self):
        print("Rendering dark theme font: Consolas, 14px")


class ThemeFactory(ABC):
    @abstractmethod
    def create_color(self) -> ThemeColor:
        pass

    @abstractmethod
    def create_font(self) -> ThemeFont:
        pass

class LightThemeFactory(ThemeFactory):
    def create_color(self):
        return LightColor()

    def create_font(self):
        return LightFont()

class DarkThemeFactory(ThemeFactory):
    def create_color(self) -> ThemeColor:
        return DarkColor()

    def create_font(self) -> ThemeFont:
        return DarkFont()


class ThemeClient:
    def __init__(self, factory: ThemeFactory):
        self.color = factory.create_color()
        self.font = factory.create_font()
    
    def apply_theme(self):
        self.color.apply()
        self.font.render()
    
print("=== Light Theme ===")
light_client = ThemeClient(LightThemeFactory())
light_client.apply_theme()

print()

print("=== Dark Theme ===")
dark_client = ThemeClient(DarkThemeFactory())
dark_client.apply_theme()