from flask import Blueprint, request
from backend.models.kb_model import list_resource
from backend.models.chat_model import save_chat, get_history
from backend.services.gemini_service import generate_answer
from backend.utils.responses import ok, error
import logging

logger = logging.getLogger(__name__)

public_bp = Blueprint('public', __name__)

@public_bp.post('/login')
def user_login():
    payload = request.get_json(silent=True) or {}
    name = payload.get('name', 'Guest')
    email = payload.get('email')
    try:
        return ok({'name': name, 'email': email}, 'User session created')
    except Exception as e:
        logger.exception('Login error')
        return error('Login failed', 500, details=str(e))


@public_bp.post('/chat')
def chat():
    payload = request.get_json(silent=True) or {}

    message = (payload.get('message') or '').strip()
    session_id = payload.get('session_id') or 'guest-session'

    if not message:
        return error('Message is required', 422)

    try:
        result = generate_answer(message)
    except Exception as e:
        logger.exception('Generate answer failed')
        return error(f"Generate Answer Error: {str(e)}", 500)

    # Save chat (don't let this crash the chatbot)
    try:
        save_chat(
            session_id,
            message,
            result['answer'],
            result.get('intent')
        )
    except Exception as e:
        logger.exception('Chat save failed')

    return ok({
        'reply': result['answer'],
        'intent': result.get('intent')
    })


@public_bp.get('/chat/history/<session_id>')
def history(session_id):
    return ok(get_history(session_id))


@public_bp.get('/courses')
def courses():
    try:
        return ok(list_resource('courses'))
    except Exception as e:
        logger.exception('List courses failed')
        return error('Failed to list courses', 500, details=str(e))


@public_bp.get('/fees')
def fees():
    try:
        return ok(list_resource('fees'))
    except Exception as e:
        logger.exception('List fees failed')
        return error('Failed to list fees', 500, details=str(e))


@public_bp.get('/placements')
def placements():
    try:
        return ok(list_resource('placements'))
    except Exception as e:
        logger.exception('List placements failed')
        return error('Failed to list placements', 500, details=str(e))


@public_bp.get('/hostel')
def hostel():
    try:
        return ok(list_resource('hostel'))
    except Exception as e:
        logger.exception('List hostel failed')
        return error('Failed to list hostel', 500, details=str(e))


@public_bp.get('/admission')
def admission():
    try:
        return ok(list_resource('admission'))
    except Exception as e:
        logger.exception('List admission failed')
        return error('Failed to list admission', 500, details=str(e))


@public_bp.get('/departments')
def departments():
    try:
        return ok(list_resource('departments'))
    except Exception as e:
        logger.exception('List departments failed')
        return error('Failed to list departments', 500, details=str(e))


@public_bp.get('/scholarships')
def scholarships():
    try:
        return ok(list_resource('scholarships'))
    except Exception as e:
        logger.exception('List scholarships failed')
        return error('Failed to list scholarships', 500, details=str(e))


@public_bp.get('/contact')
def contact():
    try:
        return ok(list_resource('contact'))
    except Exception as e:
        logger.exception('List contact failed')
        return error('Failed to list contact', 500, details=str(e))