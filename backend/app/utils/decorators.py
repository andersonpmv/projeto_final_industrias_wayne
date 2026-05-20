from functools import wraps
from flask import request, jsonify
from app.models.user import User

def role_required(cargos_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            user_id = data.get("user_id")

            if not user_id:
                return jsonify({"error": "user_id é obrigatório"}), 400

            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "Usuário não encontrado"}), 404

            if user.cargo not in cargos_permitidos:
                return jsonify({"error": "Acesso negado"}), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator