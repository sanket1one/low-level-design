"""

Association in Python OOP with MongoDB Integration:

One object needs to know about the existence of another object to perform its responsibilies.

Analogy:
student and teacher:
 - student has-A teacher 
 - teacher teaches multiple students.

 student[*] <--> teacher[1...*]


 However:

A student can still exist without a teacher.
A teacher can still exist without any specific student.
This is a real-world association:

The relationship exists.
But neither party owns the other.
Their lifecycles are independent.


Key Characteristics of Association:
- Has-a , uses-a relationship.
- Loosely coupled
- unidirectional or bidirectional

2. UML Representation:


Symbol	                Meaning	Example                                 Scenario
Solid line (---)	    An association between classes	                Student --- Teacher
Arrowhead (-->)	        Directionality (who knows whom)	                Order --> PaymentGateway
No arrowhead	        Bidirectional association	                    Team --- Developer
1	                    Exactly one	                                    Each User has one Profile
0..1	                Zero or one (optional)	                        An Employee may have a Manager
*	                    Many (zero or more)	                            A Project can have many Tasks
1..*	                At least one	                                Each Course has one or more Students

"""

from __future__ import annotations
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from mongoengine.errors import DoesNotExist

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client['hospital_db']

# Collections
rooms_collection = db['rooms']
doctors_collection = db['doctors']
patients_collection = db['patients']
appointments_collection = db['appointments']
users_collection = db['users']
messages_collection = db['messages']


def ensure_collections():
    required = ['rooms', 'doctors', 'patients', 'appointments', 'users', 'messages']
    existing = db.list_collection_names()

    for name in required:
        if name not in existing:
            db.create_collection(name)

    doctors_collection.create_index('appointments', background=True)
    patients_collection.create_index('appointments', background=True)
    appointments_collection.create_index('doctor_id', background=True)
    appointments_collection.create_index('patient_id', background=True)
    appointments_collection.create_index('room_id', background=True)
    users_collection.create_index('followers', background=True)
    users_collection.create_index('inbox', background=True)
    messages_collection.create_index('author_id', background=True)
    messages_collection.create_index('recipient_id', background=True)


ensure_collections()

# MongoEngine ODM setup for social example
connect('hospital_db', host='mongo', port=27017)


# Directional Association Example:

# 1. Unidirectional Association:

class PaymentGateway:
    def process_payment(self, amount: float) -> bool:
        print(f"Processing payment of ${amount:.2f}")
        return True

class Order:
    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway
    
    def checkout(self):
        self._gateway.process_payment(100.0)


# 2. Bidirectional Association:

"""Example: A Team has a list of Developers, and each Developer knows which Team they belong to. Either side can navigate to the other."""

class Developer:
    def __init__(self):
        self._team = None
    
    def set_team(self, team):
        self._team = team
    
class Team:
    def __init__(self):
        self._developers = []
    
    def add_developer(self, dev: Developer):
        self._developers.append(dev)
        print(self)
        dev.set_team(self)

team = Team()
dev1 = Developer()



# multiplicity example:

#. one to many

class User:
    def __init__(self, name: str):
        self._name = name
        self._groups = []
    
    def join_group(self, group):
        if group not in self._groups:
            self._groups.append(group)
            group.add_member(self)
    
class Group:
    def __init__(self, name: str):
        self._name = name
        self._users = []
    
    def add_member(self, user: User):
        if user not in self._users:
            self._users.append(user)
            user.join_group(self)

sanket = User("sanket")
aniket = User("aniket")

backend = Group("Backend Team")
frontend = Group("Frontend Team")

sanket.join_group(backend)
sanket.join_group(frontend)
aniket.join_group(backend)

"""
sanket is in : Backend Team, Frontend Team
aniket is in : Backend Team

Backend Team has members: sanket, aniket
Frontend Team has members: sanket
"""

# Example: Hospital Appointment System

"""
    Doctor || -name: String -specialization: String -appointments: List[Appointments] || + add_appointment(appointment: Appointment) : void +getPatients() :: List<Patient>
    Patient || -name: String -appointments: List[Appointments] || +add_appointment(appointment: Appointment) : void +getDoctors() :: List<Doctor>

    Doctor 1..* -> Appointments
    Patient 1..* -> Appointments

    Appointment || -doctor: Doctor -patient: Patiend -room: Room -time: String || +getDoctor(): Doctor +getPatient(): Patient +getRoom(): Room

    Appointment *..1 -> Room

    Room || -number: String -floor: int || getNumber(): String
"""

class Room:
    def __init__(self, number: str, floor: int, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self._number = number
        self._floor = floor
    
    def save(self):
        rooms_collection.replace_one(
            {'_id': self._id},
            {
                '_id': self._id,
                'number': self._number,
                'floor': self._floor
            },
            upsert=True
        )
    
    @classmethod
    def load(cls, room_id: ObjectId) -> Room:
        data = rooms_collection.find_one({'_id': room_id})
        if data:
            return cls(data['number'], data['floor'], data['_id'])
        raise ValueError("Room not found")

class Doctor:
    def __init__(self, name: str, specialization: str, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self._name = name
        self._specialization = specialization
        self._appointments = []  # List of ObjectIds
    
    def save(self):
        doctors_collection.replace_one(
            {'_id': self._id},
            {
                '_id': self._id,
                'name': self._name,
                'specialization': self._specialization,
                'appointments': self._appointments
            },
            upsert=True
        )
    
    def update_appointments(self):
        doctors_collection.update_one(
            {'_id': self._id},
            {'$set': {'appointments': self._appointments}}
        )
    
    @classmethod
    def load(cls, doctor_id: ObjectId) -> Doctor:
        data = doctors_collection.find_one({'_id': doctor_id})
        if data:
            doc = cls(data['name'], data['specialization'], data['_id'])
            doc._appointments = data.get('appointments', [])
            return doc
        raise ValueError("Doctor not found")
    
    def add_appointment(self, appointment: Appointment):
        if appointment._id not in self._appointments:
            self._appointments.append(appointment._id)
            self.update_appointments()
    
    def get_patients(self) -> List[Patient]:
        # Query appointments for this doctor, then get unique patients
        apts = list(appointments_collection.find({'doctor_id': self._id}))
        seen = set()
        result = []
        for apt in apts:
            patient_id = apt['patient_id']
            if patient_id not in seen:
                seen.add(patient_id)
                result.append(Patient.load(patient_id))
        return result

class Patient:
    def __init__(self, name: str, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self._name = name
        self._appointments = []  # List of ObjectIds
    
    def save(self):
        patients_collection.replace_one(
            {'_id': self._id},
            {
                '_id': self._id,
                'name': self._name,
                'appointments': self._appointments
            },
            upsert=True
        )
    
    def update_appointments(self):
        patients_collection.update_one(
            {'_id': self._id},
            {'$set': {'appointments': self._appointments}}
        )
    
    @classmethod
    def load(cls, patient_id: ObjectId) -> Patient:
        data = patients_collection.find_one({'_id': patient_id})
        if data:
            pat = cls(data['name'], data['_id'])
            pat._appointments = data.get('appointments', [])
            return pat
        raise ValueError("Patient not found")
    
    def add_appointment(self, appointment: Appointment):
        if appointment._id not in self._appointments:
            self._appointments.append(appointment._id)
            self.update_appointments()
    
    def get_doctors(self) -> List[Doctor]:
        # Query appointments for this patient, then get unique doctors
        apts = list(appointments_collection.find({'patient_id': self._id}))
        seen = set()
        result = []
        for apt in apts:
            doctor_id = apt['doctor_id']
            if doctor_id not in seen:
                seen.add(doctor_id)
                result.append(Doctor.load(doctor_id))
        return result


class Appointment:
    def __init__(self, doctor: Doctor, patient: Patient, room: Room, time: str, _id: Optional[ObjectId] = None, save_and_link: bool = True):
        self._id = _id or ObjectId()
        self._doctor = doctor
        self._patient = patient
        self._room = room
        self._time = time
        if save_and_link:
            self.save()
            doctor.add_appointment(self)
            patient.add_appointment(self)
    
    def save(self):
        appointments_collection.replace_one(
            {'_id': self._id},
            {
                '_id': self._id,
                'doctor_id': self._doctor._id,
                'patient_id': self._patient._id,
                'room_id': self._room._id,
                'time': self._time
            },
            upsert=True
        )
    
    @classmethod
    def load(cls, appointment_id: ObjectId) -> Appointment:
        data = appointments_collection.find_one({'_id': appointment_id})
        if data:
            doctor = Doctor.load(data['doctor_id'])
            patient = Patient.load(data['patient_id'])
            room = Room.load(data['room_id'])
            apt = cls(doctor, patient, room, data['time'], data['_id'], save_and_link=False)
            return apt
        raise ValueError("Appointment not found")


dr_smith = Doctor("Dr. Smith", "Cardiology")
dr_patel = Doctor("Dr. Patel", "Neurology")

alice = Patient("Alice")
bob = Patient("Bob")

room_101 = Room("101", 1)
room_205 = Room("205", 2)

# Save initial data
dr_smith.save()
dr_patel.save()
alice.save()
bob.save()
room_101.save()
room_205.save()

# Create appointments (this will save and update relationships)
Appointment(dr_smith, alice, room_101, "9:00 AM")
Appointment(dr_smith, bob, room_101, "10:00 AM")
Appointment(dr_patel, alice, room_205, "2:00 PM")

print(f"{dr_smith._name}'s patients:")
for p in dr_smith.get_patients():
    print(f"  - {p._name}")

print(f"{alice._name}'s doctors:")
for d in alice.get_doctors():
    print(f"  - {d._name} ({d._specialization})")

# To get schedule, query appointments directly
print(f"{dr_smith._name}'s schedule:")
apts = list(appointments_collection.find({'doctor_id': dr_smith._id}))
for apt in apts:
    patient = Patient.load(apt['patient_id'])
    room = Room.load(apt['room_id'])
    print(f"  - {apt['time']} with {patient._name} in Room {room._number}")


# social network example (MongoEngine ODM):

class Message(Document):
    author = ReferenceField('User', required=True)
    recipient = ReferenceField('User', required=True)
    content = StringField(required=True)
    timestamp = StringField(required=True)

    meta = {
        'collection': 'messages'
    }

    def send(self) -> None:
        self.save()
        recipient = self.recipient
        recipient.inbox.append(self)
        recipient.save()
        print(f"{self.author.name} -> {recipient.name}: {self.content} ({self.timestamp})")

    @classmethod
    def load(cls, message_id: ObjectId) -> Message:
        try:
            return cls.objects.get(id=message_id)
        except DoesNotExist:
            raise ValueError("Message not found")


class User(Document):
    name = StringField(required=True)
    followers = ListField(ReferenceField('User'))
    inbox = ListField(ReferenceField(Message))

    meta = {
        'collection': 'users'
    }

    def follow(self, other: 'User') -> None:
        if other == self:
            print("Cannot follow yourself.")
            return

        if other not in self.followers:
            self.followers.append(other)
            self.save()
            other.followers.append(self)
            other.save()
            print(f"{self.name} now follows {other.name}")
        else:
            print(f"{self.name} already follows {other.name}")

    def send_message(self, other: 'User', content: str, timestamp: str = "2023-10-01 12:00:00") -> None:
        if other in self.followers:
            msg = Message(author=self, recipient=other, content=content, timestamp=timestamp)
            msg.send()
        else:
            print(f"{self.name} cannot send message to {other.name} as they are not following each other.")

    def show_inbox(self) -> None:
        self.reload()
        print(f"{self.name}'s inbox:")
        for msg in self.inbox:
            print(f"  From {msg.author.name}: {msg.content} ({msg.timestamp})")


# Example usage:
alice = User(name="Alice")
alice.save()

bob = User(name="Bob")
bob.save()

alice.follow(bob)

alice.send_message(bob, "Hello Bob!", "2026-04-26 16:00:00")

bob.show_inbox()
