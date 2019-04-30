from app import db
from app.models.tables import User, Role, UserRole, Product, Category


db.create_all()