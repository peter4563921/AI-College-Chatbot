from flask import Blueprint, request
from backend.models.admin_model import find_admin_by_email
from backend.models.kb_model import RESOURCE_CONFIG, list_resource, create_resource, update_resource, delete_resource
from backend.utils.auth import make_admin_token, password_matches, admin_required
from backend.utils.responses import ok, error

admin_bp = Blueprint('admin', __name__)

@admin_bp.post('/login')
def admin_login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''
    admin = find_admin_by_email(email)
    if not admin or not password_matches(admin['password_hash'], password):
        return error('Invalid admin email or password', 401)
    token = make_admin_token(admin)
    return ok({'token': token, 'admin': {'id': admin['id'], 'name': admin['name'], 'email': admin['email']}})

@admin_bp.get('/<resource>')
@admin_required
def admin_list(resource):
    if resource not in RESOURCE_CONFIG:
        return error('Invalid resource', 404)
    return ok(list_resource(resource))

@admin_bp.post('/<resource>')
@admin_required
def admin_create(resource):
    if resource not in RESOURCE_CONFIG:
        return error('Invalid resource', 404)
    try:
        return ok(create_resource(resource, request.get_json(silent=True) or {}), 'created', 201)
    except ValueError as exc:
        return error(str(exc), 422)

@admin_bp.put('/<resource>/<int:item_id>')
@admin_required
def admin_update(resource, item_id):
    if resource not in RESOURCE_CONFIG:
        return error('Invalid resource', 404)
    try:
        return ok(update_resource(resource, item_id, request.get_json(silent=True) or {}), 'updated')
    except ValueError as exc:
        return error(str(exc), 422)

@admin_bp.delete('/<resource>/<int:item_id>')
@admin_required
def admin_delete(resource, item_id):
    if resource not in RESOURCE_CONFIG:
        return error('Invalid resource', 404)
    return ok(delete_resource(resource, item_id), 'deleted')
