import requests

from flask import Blueprint, render_template, jsonify

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("index.html")


@public_bp.route("/health")
def health():
    return jsonify({"health": "healthy"})


@public_bp.route("/map")
def live_map():
    # Logic for rendering live map
    return render_template("map.html")


@public_bp.route("/status")
def fetch_status():
    """Fetch status from MC-Core and return to the client."""
    try:
        # Make a request to the MC-Core status endpoint
        core_response = requests.get("http://mc-core:8501/status")
        core_status = core_response.json()

        # Example status for the UI service itself
        ui_status = {
            "status": "HEALTHY",
            "components": {
                "template_renderer": "HEALTHY",
                # Add other UI-related components here if needed
            },
        }

        combined_status = {"MC-Core": core_status, "MC-UI": ui_status}

        return jsonify(combined_status)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route("/task_info/<task_name>")
def fetch_task_info(task_name):
    """Fetch task information from MC-Core and return as a simple webpage."""
    try:
        # Make a request to the MC-Core task_info endpoint
        core_response = requests.get(f"http://mc-core:8501/task_info/{task_name}")
        task_info = core_response.json()

        if "server_error" in task_info:
            return render_template("error.html", message=task_info["error"])

        # Render a simple webpage with task information
        return render_template(
            "task_info.html", task_name=task_name, task_info=task_info
        )

    except requests.exceptions.RequestException as e:
        return render_template("error.html", message=str(e)), 500
