from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import blueprints
    from .public_routes import public_bp
    from .admin_routes import admin_bp

    # Register blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    return app
