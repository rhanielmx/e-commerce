from app import app, db, login_manager
from app.models.forms import ClientForm, EmployeeForm, ProductForm, CategoryForm, LoginForm
from app.models.tables import User, Client, Employee, Category, Product

from flask import render_template, redirect, url_for, request, abort, session
from flask_login import login_user, logout_user, current_user, user_logged_in, user_logged_out


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_anonymous:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                login_user(user)
            else:
                abort(400)

            return redirect(url_for('index'))

        return render_template('login.html', form=form)

    else:
        return redirect(url_for('index'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new/client', methods=['GET', 'POST'])
def new_client():

    form = ClientForm()

    name = form.name.data
    username = form.username.data
    password = form.password.data
    email = form.email.data

    if form.validate_on_submit():
        if form.password.data == request.form['repeat']:
            client = Client(name, username, password, 'client', email)
            db.session.add(client)
            db.session.commit()
        else:
            print('Senhas não coincidem!')

        return redirect(url_for('list', object='client'))

    return render_template('new_client.html', form=form)


@app.route('/update/client/<int:id>', methods=['GET', 'POST'])
def update_client(id):
    client = Client.query.filter_by(id=id).first()

    form = ClientForm()

    if client and request.method == 'POST':
        if request.form['password'] == request.form['repeat'] and request.form['password'] == client.password:
            username = request.form['username']
            name = request.form['name']
            email = request.form['email']

            client.username = username
            client.name = name
            client.email = email

            db.session.commit()

        return redirect(url_for('list', object='client'))

    return render_template('update_client.html', form=form, user=client)

@app.route('/delete/client/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    client = Client.query.filter_by(id=id).first()

    db.session.delete(client)
    db.session.commit()

    return redirect(url_for('list', object='client'))


@app.route('/new/employee', methods=['GET', 'POST'])
def new_employee():

    form = EmployeeForm()

    name = form.name.data
    username = form.username.data
    password = form.password.data
    salary = form.salary.data

    if form.validate_on_submit():
        if form.password.data == request.form['repeat']:
            employee = Employee(name, username, password, 'employee', salary)
            db.session.add(employee)
            db.session.commit()
        else:
            print('Senhas não coincidem!')

        return redirect(url_for('list', object='employee'))

    return render_template('new_employee.html', form=form)


@app.route('/update/employee/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.filter_by(id=id).first()

    form = EmployeeForm()

    if employee and request.method == 'POST':
        if request.form['password'] == request.form['repeat'] and request.form['password'] == employee.password:
            username = request.form['username']
            name = request.form['name']
            salary = request.form['salary']

            employee.username = username
            employee.name = name
            employee.salary = salary

            db.session.commit()

        return redirect(url_for('list', object='employee'))

    return render_template('update_employee.html', form=form, user=employee)


@app.route('/delete/employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    employee = Employee.query.filter_by(id=id).first()

    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for('list', object='employee'))


@app.route('/new/category', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()

    name = form.name.data
    description = form.description.data

    if form.validate_on_submit():
        category = Category(name, description)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('list', object='category'))

    return render_template('new_category.html', form=form)


@app.route('/update/category/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    category = Category.query.filter_by(id=id).first()

    form = CategoryForm()

    if category and request.method == 'POST':
        if request.form['password'] == request.form['repeat'] and request.form['password'] == current_user.password:
            name = request.form['name']
            description = request.form['description']

            category.name = name
            category.description = description

            db.session.commit()

        return redirect(url_for('list', object='category'))

    return render_template('update_category.html', form=form, category=category)


@app.route('/delete/category/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    category = Category.query.filter_by(id=id).first()

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('list', object='category'))


@app.route('/new/product', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()

    name = form.name.data
    description = form.description.data
    price = form.price.data
    category = form.category.data

    if form.validate_on_submit():
        product = Product(name, description, price, category.id)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('list', object='product'))

    return render_template('new_product.html', form=form)

@app.route('/update/product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.filter_by(id=id).first()

    form = ProductForm()

    if product and request.method == 'POST':
        if request.form['password'] == request.form['repeat'] and request.form['password'] == current_user.password:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            category_id = request.form['category']

            category = Category.query.filter_by(id=category_id).first()
            product.name = name
            product.description = description
            product.price = price
            product.category = category

            db.session.commit()

        return redirect(url_for('list', object='product'))

    return render_template('update_product.html', form=form, product=product)


@app.route('/delete/product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.filter_by(id=id).first()

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('list', object='product'))


@app.route('/list/<object>', methods=['GET', 'POST'])
def list(object):
    if object == 'client':
        objects = Client.query.all()
    elif object == 'employee':
        objects = Employee.query.all()
    elif object == 'product':
        objects = Product.query.all()
    elif object == 'category':
        objects = Category.query.all()

    return render_template('list.html', object_name=object, objects=objects)

@app.route('/update/<object>/<int:id>', methods=['GET', 'POST'])
def update(object, id):
    if object == 'client':
        return redirect(url_for('update_client', id=id))
    elif object == 'employee':
        return redirect(url_for('update_employee', id=id))
    elif object == 'product':
        return redirect(url_for('update_product', id=id))
    elif object == 'category':
        return redirect(url_for('update_category', id=id))

@app.route('/delete/<object>/<int:id>', methods=['GET', 'POST'])
def delete(object, id):
    if object == 'client':
        return redirect(url_for('delete_client', id=id))
    elif object == 'employee':
        return redirect(url_for('delete_employee', id=id))
    elif object == 'product':
        return redirect(url_for('delete_product', id=id))
    elif object == 'category':
        return redirect(url_for('delete_category', id=id))
