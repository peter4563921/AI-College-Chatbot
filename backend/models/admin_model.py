from backend.db import query

def find_admin_by_email(email):
    return query('SELECT * FROM Admins WHERE email=%s', (email,), fetchone=True)
