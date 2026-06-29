from functools import wraps
from flask import request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import check_password_hash
from backend.config import Config
from backend.utils.responses import error

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

def make_admin_token(admin):
    return serializer.dumps({'id': admin['id'], 'email': admin['email']}, salt='admin-auth')

def verify_admin_token(token):
    return serializer.loads(token, salt='admin-auth', max_age=Config.ADMIN_TOKEN_MAX_AGE_SECONDS)

def password_matches(password_hash, password):
    if password_hash == 'demo-admin123' and password == 'admin123':
        return True
    try:
        return check_password_hash(password_hash, password)
    except Exception:
        return False

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        token = header.replace('Bearer ', '').strip()
        if not token:
            return error('Admin authorization token is required', 401)
        try:
            request.admin = verify_admin_token(token)
        except SignatureExpired:
            return error('Admin session expired', 401)
        except BadSignature:
            return error('Invalid admin token', 401)
        return fn(*args, **kwargs)
    return wrapper
