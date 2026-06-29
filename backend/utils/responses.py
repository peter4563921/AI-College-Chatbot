from flask import jsonify

def ok(data=None, message='success', status=200):
    return jsonify({'status': 'success', 'message': message, 'data': data}), status

def error(message='Something went wrong', status=400, details=None):
    payload = {'status': 'error', 'message': message}
    if details:
        payload['details'] = details
    return jsonify(payload), status
