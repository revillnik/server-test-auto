from app import ma, db
from models import Employee, Holiday, Order, Auto


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        sqla_session = db.session

    employee_id = ma.auto_field(dump_only=True)


schema_for_all_employees = EmployeeSchema(many=True)
schema_for_one_employee = EmployeeSchema(many=False)


class HolidaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Holiday
        load_instance = True
        sqla_session = db.session

    holiday_id = ma.auto_field(dump_only=True)


schema_for_all_holidays = HolidaySchema(many=True)
schema_for_one_holiday = HolidaySchema(many=False)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session

    order_id = ma.auto_field(dump_only=True)


schema_for_all_orders = OrderSchema(many=True)
schema_for_one_order = OrderSchema(many=False)


class AutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Auto
        load_instance = True
        sqla_session = db.session

    auto_id = ma.auto_field(dump_only=True)


schema_for_all_autos = AutoSchema(many=True)
schema_for_one_auto = AutoSchema(many=False)
