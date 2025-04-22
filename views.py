from app import app, db, login_manager
from models import Employee, Holiday, Order, Auto, User
from serializers import (
    schema_for_all_employees,
    schema_for_one_employee,
    schema_for_all_holidays,
    schema_for_one_holiday,
    schema_for_all_orders,
    schema_for_one_order,
    schema_for_all_autos,
    schema_for_one_auto,
    schema_for_one_user,
)
from flask import request
from datetime import datetime
from sqlalchemy import func
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():
    return "first page"


@app.route("/all_employees")
def all_employees():
    query_with_all_employees = db.session.query(Employee).all()
    data_all_employees = schema_for_all_employees.dump(query_with_all_employees)
    return data_all_employees


@app.route("/all_employees_without_holiday")
def all_employees_without_holiday():
    date_now = datetime.now().date()
    query_with_all_employees_without_holiday = (
        db.session.query(Employee)
        .join(Holiday)
        .filter((Holiday.date_out < date_now) | (Holiday.date_on > date_now))
        .all()
    )
    data_all_employees_without_holiday = schema_for_all_employees.dump(
        query_with_all_employees_without_holiday
    )
    return data_all_employees_without_holiday


@app.route("/max_min_sale_auto_employees")
def max_min_statictic_employees():
    query_for_sale_employee = (
        db.session.query(Order.employee_id, func.count(Auto.auto_id))
        .join(Auto)
        .group_by(Order.employee_id)
        .all()
    )
    data_max_min_sale_auto_employee = {
        "max_sale": {
            "count_of_autos": query_for_sale_employee[0][1],
            "employee_information": schema_for_one_employee.dump(
                db.session.query(Employee).get(query_for_sale_employee[0][0])
            ),
        },
        "min_sale": {
            "count_of_autos": query_for_sale_employee[-1][1],
            "employee_information": schema_for_one_employee.dump(
                db.session.query(Employee).get(query_for_sale_employee[-1][0])
            ),
        },
    }
    return data_max_min_sale_auto_employee


@app.route("/with_without_holidays_employees")
def with_without_holidays_employees():
    query_for_without_employees = (
        db.session.query(Employee)
        .outerjoin(Holiday)
        .filter(Holiday.holiday_id.is_(None))
        .all()
    )
    query_for_with_employees = db.session.query(Employee).join(Holiday).all()

    data_with_without_employees = {
        "without_employees": schema_for_all_employees.dump(query_for_without_employees),
        "with_employees": schema_for_all_employees.dump(query_for_with_employees),
    }
    return data_with_without_employees


@app.route("/employee/<int:employee_id>")
def employee(employee_id):
    query_with_one_employee = db.session.query(Employee).get_or_404(employee_id)
    data_one_employee = schema_for_one_employee.dump(query_with_one_employee)
    return data_one_employee


@app.route("/all_holidays")
def all_holidays():
    query_with_all_holidays = db.session.query(Holiday).all()
    data_all_holidays = schema_for_all_holidays.dump(query_with_all_holidays)
    return data_all_holidays


@app.route("/holiday/<int:holiday_id>")
def holiday(holiday_id):
    query_with_one_holiday = db.session.query(Holiday).get_or_404(holiday_id)
    data_one_holiday = schema_for_one_holiday.dump(query_with_one_holiday)
    return data_one_holiday


@app.route("/all_orders")
def all_orders():
    query_with_all_orders = db.session.query(Order).all()
    data_all_orders = schema_for_all_orders.dump(query_with_all_orders)
    return data_all_orders


@app.route("/orders_buy_and_no_car")
def orders_buy_and_no_car():
    query_with_orders_buy_car = (
        db.session.query(Order, func.count(Auto.auto_id))
        .outerjoin(Auto)
        .group_by(Order.order_id)
        .all()
    )
    data_withs_orders_buy_and_no_car = {
        "with_car": [
            {
                "order": schema_for_one_order.dump(query_with_orders_buy_car[i][0]),
                "count_autos": query_with_orders_buy_car[i][1],
            }
            for i in range(len(query_with_orders_buy_car))
            if query_with_orders_buy_car[i][1]
        ],
        "without_car": [
            {
                "order": schema_for_one_order.dump(query_with_orders_buy_car[i][0]),
                "count_autos": query_with_orders_buy_car[i][1],
            }
            for i in range(len(query_with_orders_buy_car))
            if not query_with_orders_buy_car[i][1]
        ],
    }

    return data_withs_orders_buy_and_no_car


@app.route("/order_max_money")
@app.route("/order_min_money")
@app.route("/orders_money")
def orders_min_max_all_money():
    query_with_orders_money = (
        db.session.query(Order, func.sum(Auto.price))
        .join(Auto)
        .group_by(Order.order_id)
        .order_by(func.sum(Auto.price))
        .all()
    )
    data_with_orders_money = [
        {
            "order": schema_for_one_order.dump(query_with_orders_money[i][0]),
            "sum_price": query_with_orders_money[i][1],
        }
        for i in range(len(query_with_orders_money))
    ]
    if str(request.url_rule) == "/order_min_money":
        return data_with_orders_money[0]
    elif str(request.url_rule) == "/order_max_money":
        return data_with_orders_money[-1]
    else:
        return data_with_orders_money


@app.route("/order/<int:order_id>")
def order(order_id):
    query_with_one_order = db.session.query(Order).get_or_404(order_id)
    data_one_order = schema_for_one_order.dump(query_with_one_order)
    return data_one_order


@app.route("/all_autos")
def all_autos():
    query_with_all_autos = db.session.query(Auto).all()
    data_all_autos = schema_for_all_autos.dump(query_with_all_autos)
    return data_all_autos


@app.route("/auto/<int:auto_id>")
def auto(auto_id):
    query_with_one_auto = db.session.query(Auto).get_or_404(auto_id)
    data_one_auto = schema_for_one_auto.dump(query_with_one_auto)
    return data_one_auto


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return "Отправьте POST запросом username и password"
    elif request.method == "POST":
        check_user = (
            db.session.query(User)
            .filter(User.username == request.json.get("username"))
            .one()
        )
        if check_user and check_user.check_password(request.json.get("password")):
            login_user(check_user)
            return f"Успешный вход пользователя {current_user.username}"
        else:
            return "Пользователь не найден"


@app.route("/logout")
def logout():
    logout_user()
    return "Вы вышли из аккаунта"


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return "Отправьте для регистрации POST запросом username, email, password"
    elif request.method == "POST":
        request.json["password_hash"] = generate_password_hash(request.json["password"])
        del request.json["password"]
        create_user = schema_for_one_user.load(request.json)
        db.session.add(create_user)
        db.session.flush()
        db.session.commit()
        return f"Успешно создан пользователь {create_user.username}"


@app.route("/profile")
@login_required
def profile():
    data_user = schema_for_one_user.dump(current_user)
    return data_user
