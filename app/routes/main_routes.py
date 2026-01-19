from flask import Blueprint, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    if current_user.rol == "campo":
        return redirect(url_for("campo.dashboard"))

    if current_user.rol == "data":
        return redirect(url_for("data.dashboard"))

    return redirect(url_for("auth.login"))
