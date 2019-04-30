from app import db

class Base(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

"""
class Type(Base):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    clients = db.relationship("Client", back_populates="role")
    employees = db.relationship("Employee", back_populates="types")
""";

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    type = db.Column(db.String(50))

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    __mapper_args__ = {
        'polymorphic_identity':'users',
        'polymorphic_on':type
    }


class Client(User):
    client_name = db.Column(db.String(100))

    def __init__(self, username, password, type,  client_name):
        super().__init__(username, password, type)
        self.client_name = client_name

    __mapper_args__ = {
        'polymorphic_identity':'client',
    }


class Employee(User):
    salary = db.Column(db.Float(precision=2))

    def __init__(self, username, password, type, salary):
        super().__init__(username, password, type)
        self.salary = salary

    __mapper_args__ = {
        'polymorphic_identity':'employee'
    }
