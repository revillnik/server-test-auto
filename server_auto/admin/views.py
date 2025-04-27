from flask import Blueprint, request
from server_auto.models import User
from server_auto.serializers import schema_for_one_user
from server_auto import db, login_manager
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
    LoginManager,
)
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint("admin", __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@admin.route("/login", methods=["POST", "GET"])
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


@admin.route("/logout")
def logout():
    logout_user()
    return "Вы вышли из аккаунта"


@admin.route("/register", methods=["POST", "GET"])
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


@admin.route("/profile")
@login_required
def profile():
    data_user = schema_for_one_user.dump(current_user)
    return data_user
