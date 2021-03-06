from app import app, db, login_manager
from app.models.forms import ClientForm, EmployeeForm, ProductForm, CategoryForm, LoginForm
from app.models.tables import *

from flask import render_template, redirect, url_for, request, abort, session, make_response
from flask_login import login_user, logout_user, current_user, user_logged_in, user_logged_out, login_fresh

from functools import wraps

import json

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print(current_user.is_authenticated)
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            if ((current_user.type != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
@login_required()
def menu():
    return render_template('lists.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_anonymous:
        form = LoginForm()
        next = request.args.get('next')

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                login_user(user)
            else:
                abort(400)

            return redirect(next or url_for('index'))

        return render_template('login.html', form=form)

    else:
        return redirect(url_for('index'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile/<int:id>")
def profile(id):
    user = User.query.filter_by(id=id).first()
    if user.type == 'client':
        return redirect(url_for('update_client', id=id))
    if user.type == 'employee':
        return redirect(url_for('update_employee', id=id))


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
def delete_client(id):
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
@login_required(role='employee')
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

    if request.method=='POST':
        id = request.form['user_id']
        employee = Employee.query.filter_by(id=id).first()
        print(employee)

        db.session.delete(employee)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/new/category', methods=['GET', 'POST'])
@login_required(role='employee')
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
@login_required(role='employee')
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
@login_required(role='employee')
def delete_category(id):
    category = Category.query.filter_by(id=id).first()

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('list', object='category'))


@app.route('/new/product', methods=['GET', 'POST'])
@login_required(role='employee')
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
@login_required(role='employee')
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
@login_required(role='employee')
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
@login_required(role='employee')
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
@login_required(role='employee')
def delete(object, id):
    if object == 'client':
        return redirect(url_for('delete_client', id=id))
    elif object == 'employee':
        return redirect(url_for('delete_employee', id=id))
    elif object == 'product':
        return redirect(url_for('delete_product', id=id))
    elif object == 'category':
        return redirect(url_for('delete_category', id=id))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    query=request.args.get('query')
    results = []
    category = Category.query.filter(Category.name.like(f'%{query}%')).first()
    products_like = Product.query.filter(Product.name.like(f'%{query}%')).all()
    products_contains = Product.query.filter(Product.name.contains(query)).all()

    if category:
        products = Product.query.filter_by(category_id=category.id).all()
        for product in products:
            results.append(product)

    if products_like:
        for product in products_like:
            if product not in results: results.append(product)

    if products_contains:
        for product in products_contains:
            if product not in results: results.append(product)

    return render_template('search.html', products=results)

@app.route('/carrinho', methods=['GET', 'POST'])
def add_to_cart():

    exists = False

    resp = request.cookies.get('shopping-cart')

    total_price = 0

    if resp is not None:
        for item in json.loads(resp):
            total_price += float(item['price']) * int(item['quantity'])

    if request.method=='POST':
        product = request.form['product']
        category = request.form['category']
        price = request.form['price']
        id = request.form['id[]']

        if resp is None:
            cart = [{
                'id': id,
                'product': product,
                'category': category,
                'price': price,
                'quantity': 1
            }]

            resp = json.dumps(cart)
            response = make_response(render_template('carrinho.html', products = cart, price=total_price))
            response.set_cookie('shopping-cart', resp, max_age=60*60*24*365*2)
            return response
        else:
            cart = json.loads(resp)
            for item in cart:
                if item['product'] == product:
                    item['quantity'] += 1
                    total_price += float(item['price'])
                    exists = True

            if not exists:
                new_item = {
                    'id': id,
                    'product': product,
                    'category': category,
                    'price': price,
                    'quantity': 1,
                }
                print(new_item)
                cart.append(new_item)
                total_price += float(new_item['price'])

            resp = json.dumps(cart)

            response = make_response(render_template('carrinho.html', products = cart, price=total_price))
            response.set_cookie('shopping-cart', resp, max_age= 60 * 60 * 24 * 365 * 2)
            return response

    return render_template('carrinho.html', products=json.loads(resp), price=total_price)

@app.route('/remove', methods=['GET', 'POST'])
def remove_from_cart():

    resp = request.cookies.get('shopping-cart')

    cart = json.loads(resp)
    total_price = 0

    if resp is not None:
        for item in json.loads(resp):
            total_price += float(item['price']) * int(item['quantity'])

    if request.method == 'POST':
        id = request.form['id[]']

        for item in cart:
            if item['id'] == id and item['quantity'] > 0:
                item['quantity'] -= 1
                total_price -= float(item['price'])

        resp = json.dumps(cart)

        response = make_response(render_template('carrinho.html', products=cart, price=total_price))
        response.set_cookie('shopping-cart', resp, max_age=60 * 60 * 24 * 365 * 2)
        return response

    return render_template('carrinho.html', products=cart, price=total_price)

@app.route('/get_cookies', methods=['GET', 'POST'])
def get_cookies():
    resp = request.cookies.get('shopping-cart')
    return resp or 'oi'

@app.route('/finalizar compra', methods = ['GET', 'POST'])
def finalizar_compra():
    user_id = current_user.id
    resp = request.cookies.get('shopping-cart')
    iterador = json.loads(resp)
    produtos = ''
    price = 0.0
    for item in iterador:
        produtos = produtos + str(item['product']) + ' - (' + str(item['quantity']) + ' Unidade(s))  '
        price = price + (float(item['price']) * float(item['quantity']))
    query = """INSERT INTO bags (price, products,user_id)
                VALUES({0},'{1}',{2})
            """.format(price, produtos, user_id)
    db.session.execute(query)
    db.session.commit()

    resp = make_response(render_template('finalizar_compra.html'))
    resp.set_cookie('shopping-cart','', expires = 0)
    return resp

@app.route('/listar_compras', methods = ['GET','POST'])
def render_compras():
    user_id = current_user.id
    query = """ Select price, products from bags
                where user_id = {0}
            """.format(user_id)
    compras = db.session.execute(query)
    items = []
    for item in compras:
        items.append(item)
    return render_template('suas_compras.html', items = items)
    
    