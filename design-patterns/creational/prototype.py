"""

Builder:

creating new object by cloning existing ones.

Self-cloning: The object itself knows how to create a copy of itlself.
No External code need to understand it's internal structure.

Decoupled creation: The client doesn't need to know the concrete class of the object  it is cloning,



Class Diagram for Prototype Pattern
====================================
            +---------------------+
            |       Client        |
            +---------------------+
            | -prototype: Prototype |
            +---------------------+
            | +operation()        |
            +---------------------+
                    | implements
                    |
            +---------------------+
            |    «interface»      |
            |     Prototype       |
            +---------------------+
            | +clone(): Prototype |
            +---------------------+
          ^
          | implements
          |
+---------------------+     +---------------------+
| ConcretePrototypeA  |     | ConcretePrototypeB  |
+---------------------+     +---------------------+
| -fieldA: String     |     | -fieldX: double     |
| -fieldB: int        |     | -fieldY: List       |
+---------------------+     +---------------------+
| +clone(): Prototype |     | +clone(): Prototype |
+---------------------+     +---------------------+


"""
# Email Template

"""
Let us apply Prototype to a completely different domain. You are building a bulk email system. Your company sends a monthly newsletter, but each department needs a slightly different version with a customized subject line and department-specific recipients.

The base template defines the shared body text and a default recipient list, and you clone it for each department variant.

Without Prototype, you would duplicate the full constructor call for every department email, copying all the shared fields each time. With Prototype, you define the base template once and clone it for each variant.

The key challenge is that RecipientList is a nested mutable object containing two lists: to and cc. A shallow clone would cause all email templates to share the same recipient lists, so adding a recipient to the marketing email would also add them to every other department's email.
"""

class RecipientList:
    def __init__(self, to, cc):
        self.to = list(to)
        self.cc = list(cc)
    
    def deep_copy(self):
        return RecipientList(list(self.to), list(self.cc))

    def add_to(self, email):
        self.to.append(email)

    def add_cc(self, email):
        self.cc.append(email)

    def __repr__(self):
        return f"{{to={self.to}, cc={self.cc}}}"


class EmailTemplate:
    def __init__(self, subject, body, recipients):
        self.subject = subject
        self.body = body
        self.recipients = recipients

    def clone(self):
        return EmailTemplate(self.subject, self.body, self.recipients.deep_copy())

    def print_email(self):
        print(f"Email: {self.subject} | Recipients: {self.recipients}")
    
base_recipients = RecipientList(["all@company.com"], ["archive@company.com"])
base_template = EmailTemplate(
    "Company Newsletter", "Monthly updates from the team...", base_recipients)

marketing_email = base_template.clone()
marketing_email.subject = "Marketing news letter"
marketing_email.recipients.add_to("marketing@company.com")

engineering_email = base_template.clone()
engineering_email.subject = "Engineering Newsletter"
engineering_email.recipients.add_to("eng-team@company.com")

hr_email = base_template.clone()
hr_email.subject = "HR Newsletter"
hr_email.recipients.add_to("hr@company.com")
hr_email.recipients.add_cc("ceo@company.com")


marketing_email.print_email()
engineering_email.print_email()
hr_email.print_email()

print("\nBase template unchanged:")
base_template.print_email()


from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Circle(Cloneable):
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius

    def clone(self):
        return Circle(self.color, self.radius)

    def print_info(self):
        print(f"Circle [Color: {self.color}, Radius: {self.radius}]")

class Rectangle(Cloneable):
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height

    def clone(self):
        return Rectangle(self.color, self.width, self.height)

    def print_info(self):
        print(f"Rectangle [Color: {self.color}, Width: {self.width}, Height: {self.height}]")
