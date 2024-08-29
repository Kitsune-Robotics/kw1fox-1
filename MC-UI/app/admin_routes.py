from flask import Blueprint, render_template, request, Response
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Basic auth decorator
def check_auth(username, password):
    return username == "admin" and password == "password"


def authenticate():
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/")
@requires_auth
def admin_index():
    return render_template("admin.html")


@admin_bp.route("/run-command")
@requires_auth
def run_command():
    # Logic to run commands or debug
    return "Command executed."
