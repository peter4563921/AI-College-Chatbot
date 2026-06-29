from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.controllers.public_controller import public_bp
from backend.controllers.admin_controller import admin_bp
from backend.utils.responses import ok, error

import traceback

app = Flask(__name__)
app.config.from_object(Config)

# ===========================
# DEBUG CONFIG
# ===========================
print("=" * 60)
print("MYSQL_HOST     :", Config.MYSQL_HOST)
print("MYSQL_PORT     :", Config.MYSQL_PORT)
print("MYSQL_USER     :", Config.MYSQL_USER)
print("MYSQL_PASSWORD :", Config.MYSQL_PASSWORD)
print("MYSQL_DATABASE :", Config.MYSQL_DATABASE)
print("GEMINI_MODEL   :", Config.GEMINI_MODEL)
print("=" * 60)

# ===========================
# Enable CORS
# ===========================
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# ===========================
# Register Routes
# ===========================
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

# ===========================
# Home
# ===========================
@app.route("/", methods=["GET"])
def home():
    return ok({
        "name": "AI Powered College Enquiry Chatbot",
        "version": "1.0.0"
    })

# ===========================
# Health Check
# ===========================
@app.route("/health", methods=["GET"])
def health():
    return ok({
        "healthy": True
    })

# ===========================
# 404
# ===========================
@app.errorhandler(404)
def not_found(e):
    return error(
        message="Endpoint not found",
        status=404
    )

# ===========================
# Global Exception
# ===========================
@app.errorhandler(Exception)
def handle_exception(exc):

    print("\n")
    print("=" * 60)
    print("SERVER ERROR")
    print("=" * 60)

    traceback.print_exc()

    print("=" * 60)

    return error(
        message="Internal server error",
        status=500,
        details=str(exc)
    )

# ===========================
# Start Server
# ===========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )