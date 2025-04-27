from server_auto import db
from server_auto.models import Employee, Holiday, Order, Auto
from server_auto.serializers import (
    schema_for_all_employees,
    schema_for_one_employee,
    schema_for_all_holidays,
    schema_for_one_holiday,
    schema_for_all_orders,
    schema_for_one_order,
    schema_for_all_autos,
    schema_for_one_auto,
)
from flask import request, Blueprint
from datetime import datetime
from sqlalchemy import func

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "first page"


@main.route("/all_employees")
def all_employees():
    query_with_all_employees = db.session.query(Employee).all()
    data_all_employees = schema_for_all_employees.dump(query_with_all_employees)
    return data_all_employees


@main.route("/all_employees_without_holiday")
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


@main.route("/max_min_sale_auto_employees")
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


@main.route("/with_without_holidays_employees")
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


@main.route("/employee/<int:employee_id>")
def employee(employee_id):
    query_with_one_employee = db.session.query(Employee).get_or_404(employee_id)
    data_one_employee = schema_for_one_employee.dump(query_with_one_employee)
    return data_one_employee


@main.route("/all_holidays")
def all_holidays():
    query_with_all_holidays = db.session.query(Holiday).all()
    data_all_holidays = schema_for_all_holidays.dump(query_with_all_holidays)
    return data_all_holidays


@main.route("/holiday/<int:holiday_id>")
def holiday(holiday_id):
    query_with_one_holiday = db.session.query(Holiday).get_or_404(holiday_id)
    data_one_holiday = schema_for_one_holiday.dump(query_with_one_holiday)
    return data_one_holiday


@main.route("/all_orders")
def all_orders():
    query_with_all_orders = db.session.query(Order).all()
    data_all_orders = schema_for_all_orders.dump(query_with_all_orders)
    return data_all_orders


@main.route("/orders_buy_and_no_car")
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


@main.route("/order_max_money")
@main.route("/order_min_money")
@main.route("/orders_money")
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


@main.route("/order/<int:order_id>")
def order(order_id):
    query_with_one_order = db.session.query(Order).get_or_404(order_id)
    data_one_order = schema_for_one_order.dump(query_with_one_order)
    return data_one_order


@main.route("/all_autos")
def all_autos():
    query_with_all_autos = db.session.query(Auto).all()
    data_all_autos = schema_for_all_autos.dump(query_with_all_autos)
    return data_all_autos


@main.route("/auto/<int:auto_id>")
def auto(auto_id):
    query_with_one_auto = db.session.query(Auto).get_or_404(auto_id)
    data_one_auto = schema_for_one_auto.dump(query_with_one_auto)
    return data_one_auto
