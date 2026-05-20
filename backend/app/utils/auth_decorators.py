from functools import wraps
from flask import request, jsonify
from app.utils.auth import validar_token

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token não informado"}), 401

        try:
            token = auth_header.split(" ")[1]
        except:
            return jsonify({"error": "Token inválido"}), 401

        user_id = validar_token(token)

        if not user_id:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        return func(user_id, *args, **kwargs)

    return wrapper