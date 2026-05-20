from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db, bcrypt
from app.utils.auth import gerar_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not user.ativo:
        return jsonify({"error": "Usuário inativo"}), 403

    if not user.acesso_ativo:
        return jsonify({"error": "Acesso revogado. Procure o administrador."}), 403

    if not bcrypt.check_password_hash(user.senha, senha):
        return jsonify({"error": "Senha incorreta"}), 401

    token = gerar_token(user)

    return jsonify({
        "message": "Login realizado com sucesso",
        "token": token,
        "cargo": user.cargo,
        "nome": user.nome
}), 200