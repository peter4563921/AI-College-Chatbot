from backend.db import query

def save_chat(session_id, user_message, bot_response, intent=None, user_id=None):
    query(
        'INSERT INTO ChatHistory (session_id, user_id, user_message, bot_response, intent) VALUES (%s, %s, %s, %s, %s)',
        (session_id, user_id, user_message, bot_response, intent),
        commit=True,
    )

def get_history(session_id, limit=30):
    return query('SELECT user_message, bot_response, intent, created_at FROM ChatHistory WHERE session_id=%s ORDER BY id DESC LIMIT %s', (session_id, limit))
