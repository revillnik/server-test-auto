from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class Employee(db.Model):
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    phone = db.Column(db.String(64), nullable=False)

    orders = db.relationship("Order", backref="employee")
    holiday = db.relationship("Holiday", backref="employee", uselist=False)

    def __repr__(self):
        return f"employee_id: {self.employee_id} name: {self.name} "


class Holiday(db.Model):
    __tablename__ = "holidays"
    holiday_id = db.Column(db.Integer(), primary_key=True)
    date_on = db.Column(db.Date(), nullable=False)
    date_out = db.Column(db.Date(), nullable=False)

    employee_id = db.Column(db.Integer(), db.ForeignKey("employees.employee_id"))

    def __repr__(self):
        return f"date_on: {self.date_on} date_out: {self.date_out} "


class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer(), primary_key=True)
    order_date = db.Column(db.Date(), nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    phone = db.Column(db.String(64), nullable=False, unique=True)
    adress = db.Column(db.String(255), nullable=False)

    employee_id = db.Column(db.Integer(), db.ForeignKey("employees.employee_id"))

    autos = db.relationship("Auto", backref="order")

    def __repr__(self):
        return f"order_id: {self.order_id} first_name and last_name: {self.first_name} {self.last_name} "


class Auto(db.Model):
    __tablename__ = "autos"
    auto_id = db.Column(db.Integer(), primary_key=True)
    mark = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)

    order_id = db.Column(db.Integer(), db.ForeignKey("orders.order_id"))

    def __repr__(self):
        return f"auto_id: {self.auto_id} mark and model: {self.mark} {self.model} "


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    may_create = db.Column(db.Boolean(), default=True)
    may_update = db.Column(db.Boolean(), default=True)
    may_delete = db.Column(db.Boolean(), default=True)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None
