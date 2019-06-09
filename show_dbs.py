from app import db
from app.models.tables import User, Client, Employee, Product, Category

"""
users = User.query.all()
products = Product.query.all()
categories = Category.query.all()

relationships = UserRole.query.all()
"""

#db.create_all()

query = 'Livro'
category = Category.query.filter(Category.name.like(f'%{query}%')).first()
categories = Category.query.all()
print([category.name for category in categories])
print(category)
#users = User.query.all()
#employee = Employee.query.filter_by(name='Apagar').first()
#print(employee)

#db.session.delete(employee)
#db.session.commit()
#print(employee)

#print(Category.query.filter(Category.name.ilike('%' + 'Livr' + '%')).first().get_id())
#print(Category.query.filter_by(name='Livros').first().get_id())