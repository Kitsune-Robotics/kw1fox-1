import requests

from flask import Blueprint, render_template, jsonify

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("index.html")


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
