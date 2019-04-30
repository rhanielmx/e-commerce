from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app import db
from app.models.tables import Category



class ClientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])

class EmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    salary = FloatField('salary', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])


def category_choices():
    return db.session.query(Category).all()


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    price = FloatField("price", validators=[DataRequired()])
    category = QuerySelectField("category", validators=[DataRequired()], query_factory=category_choices)
