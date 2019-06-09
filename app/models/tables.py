from app import db


"""
class Type(Base):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    clients = db.relationship("Client", back_populates="role")
    employees = db.relationship("Employee", back_populates="types")
""";


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    type = db.Column(db.String(50))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __init__(self, name, username, password, type):
        self.name = name
        self.username = username
        self.password = password
        self.type = type

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }


class Client(User):
    email = db.Column(db.String(100))

    def __init__(self, name, username, password, type,  email):
        super().__init__(name, username, password, type)
        self.email = email

    __mapper_args__ = {
        'polymorphic_identity':'client',
    }


class Employee(User):
    salary = db.Column(db.Float(precision=2))

    def __init__(self, name, username, password, type, salary):
        super().__init__(name, username, password, type)
        self.salary = salary

    __mapper_args__ = {
        'polymorphic_identity':'employee'
    }

#class Role(db.Model):
#    __tablename__ = 'roles'
#    id = db.Column(db.Integer(), primary_key=True)
#    name = db.Column(db.String(50), unique=True)
#
#    def __init__(self, name):
#        self.name = name

#    def __repr__(self):
#       return '<Role %r>' % self.name


#class UserRole(db.Model):
#    __tablename__ = 'user_roles'
#    id = db.Column(db.Integer(), primary_key=True)
#    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

#    def __init__(self, user_id, role_id):
#        self.user_id = user_id
#        self.role_id = role_id

#    def __repr__(self):
#        return '<User-Role {}-{}>'.format(self.user_id, self.role_id)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float(precision=2))
    category_id = db.Column(db.String(), db.ForeignKey('categories.id', ondelete='NO ACTION', onupdate='CASCADE'))

    category = db.relationship('Category', foreign_keys=category_id)

    def __init__(self, name, description, price, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return "<Product %r>" % self.name

class Bag(db.Model):
    __tablename__ = 'bags'

    id = db.Column(db.Integer(), primary_key = True)
    isPurchased = db.Column(db.Boolean(), unique = False, nullable = False)
    price = db.Column(db.Float(precision = 2))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete = 'NO ACTION', onupdate='NO ACTION'))

    user = db.relationship('User', foreign_keys = user_id)

    def __init__(self, isPurchased, price, user_id):
        self.isPurchased = isPurchased
        self.price = price,
        self.user_id = user_id

 