from flask import Blueprint, render_template

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("index.html")


@public_bp.route("/map")
def live_map():
    # Logic for rendering live map
    return render_template("map.html")
