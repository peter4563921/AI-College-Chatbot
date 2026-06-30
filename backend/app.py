from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import Config
from backend.controllers.public_controller import public_bp
from backend.controllers.admin_controller import admin_bp
from backend.utils.responses import ok, error
from flask import request
import logging

import os
import traceback

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app.config.from_object(Config)

# ============================================
# DEBUG CONFIG
# ============================================
print("=" * 60)
print("MYSQL_HOST     :", Config.MYSQL_HOST)
print("MYSQL_PORT     :", Config.MYSQL_PORT)
print("MYSQL_USER     :", Config.MYSQL_USER)
print("MYSQL_PASSWORD :", Config.MYSQL_PASSWORD)
print("MYSQL_DATABASE :", Config.MYSQL_DATABASE)
print("GEMINI_MODEL   :", Config.GEMINI_MODEL)
print("=" * 60)

# ============================================
# Enable CORS
# ============================================
# Use configured origins (comma separated) or '*' for all
origins = Config.CORS_ORIGINS or '*'
if isinstance(origins, str) and origins != '*':
    origins = [o.strip() for o in origins.split(',') if o.strip()]

# Only expose API endpoints to configured origins
CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    supports_credentials=(origins != '*')
)

# ============================================
# Register API Routes
# ============================================
app.register_blueprint(public_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")


# Log all requests
@app.before_request
def log_request_info():
    logger.info('Incoming %s %s from %s', request.method, request.path, request.remote_addr)
    logger.info('Headers: %s', dict(request.headers))
    try:
        logger.info('Body: %s', request.get_data(as_text=True))
    except Exception:
        pass

# ============================================
# Frontend Routes
# ============================================

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/admin")
def admin():
    return send_from_directory(app.static_folder, "admin.html")


@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(
        os.path.join(app.static_folder, "css"),
        filename
    )


@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(
        os.path.join(app.static_folder, "js"),
        filename
    )


# ============================================
# API INFO
# ============================================

@app.route("/api", methods=["GET"])
def api_home():
    return ok({
        "name": "AI Powered College Enquiry Chatbot",
        "version": "1.0.0"
    })


# ============================================
# Health Check
# ============================================

@app.route("/health", methods=["GET"])
def health():
    return ok({
        "healthy": True
    })


# ============================================
# 404
# ============================================

@app.errorhandler(404)
def not_found(e):
    return error(
        message="Endpoint not found",
        status=404
    )


# ============================================
# Global Exception
# ============================================

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


# ============================================
# Start Server
# ============================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )