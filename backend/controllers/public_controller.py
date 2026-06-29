from flask import Blueprint, request
from backend.models.kb_model import list_resource
from backend.models.chat_model import save_chat, get_history
from backend.services.gemini_service import generate_answer
from backend.utils.responses import ok, error

public_bp = Blueprint('public', __name__)

@public_bp.post('/login')
def user_login():
    payload = request.get_json(silent=True) or {}
    name = payload.get('name', 'Guest')
    email = payload.get('email')
    return ok({'name': name, 'email': email}, 'User session created')


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
        print("Chat save failed:", e)

    return ok({
        'reply': result['answer'],
        'intent': result.get('intent')
    })


@public_bp.get('/chat/history/<session_id>')
def history(session_id):
    return ok(get_history(session_id))


@public_bp.get('/courses')
def courses():
    return ok(list_resource('courses'))


@public_bp.get('/fees')
def fees():
    return ok(list_resource('fees'))


@public_bp.get('/placements')
def placements():
    return ok(list_resource('placements'))


@public_bp.get('/hostel')
def hostel():
    return ok(list_resource('hostel'))


@public_bp.get('/admission')
def admission():
    return ok(list_resource('admission'))


@public_bp.get('/departments')
def departments():
    return ok(list_resource('departments'))


@public_bp.get('/scholarships')
def scholarships():
    return ok(list_resource('scholarships'))


@public_bp.get('/contact')
def contact():
    return ok(list_resource('contact'))