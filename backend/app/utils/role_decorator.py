from functools import wraps
from flask import jsonify
from app.models.user import User

def role_required(*cargos_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(user_id, *args, **kwargs):
            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "Usuário não encontrado"}), 404

            if user.cargo not in cargos_permitidos:
                return jsonify({"error": "Acesso negado"}), 403

            return func(user_id, *args, **kwargs)

        return wrapper
    return decorator