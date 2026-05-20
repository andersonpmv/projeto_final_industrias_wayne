from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from app.utils.auth_decorators import token_required
from app.utils.role_decorator import role_required

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@token_required
@role_required("admin")
def listar_usuarios(user_id):

    usuarios = User.query.all()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "ativo": usuario.ativo,
            "acesso_ativo": usuario.acesso_ativo
        })

    return jsonify(resultado), 200


@user_bp.route("/users", methods=["POST"])
@token_required
@role_required("admin")
def criar_usuario(user_id):

    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    cargo = data.get("cargo")

    if not nome or not email or not senha or not cargo:
        return jsonify({
            "error": "nome, email, senha e cargo são obrigatórios"
        }), 400

    cargos_validos = ["funcionario", "gerente"]

    if cargo not in cargos_validos:
        return jsonify({
            "error": "cargo inválido"
        }), 400

    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente:
        return jsonify({
            "error": "email já cadastrado"
        }), 400

    senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    novo_usuario = User(
        nome=nome,
        email=email,
        senha=senha_hash,
        cargo=cargo,
        ativo=True,
        acesso_ativo=True
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário criado com sucesso"
    }), 201


@user_bp.route("/users/<int:id>", methods=["PUT"])
@token_required
@role_required("admin")
def atualizar_usuario(user_id, id):

    usuario = User.query.get(id)

    if not usuario:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404

    data = request.get_json()

    cargo = data.get("cargo", usuario.cargo)

    cargos_validos = ["funcionario", "gerente", "admin"]

    if cargo not in cargos_validos:
        return jsonify({
            "error": "cargo inválido"
        }), 400

    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)
    usuario.cargo = cargo

    if data.get("senha"):
        usuario.senha = bcrypt.generate_password_hash(
            data.get("senha")
        ).decode("utf-8")

    db.session.commit()

    return jsonify({
        "message": "Usuário atualizado com sucesso"
    }), 200


@user_bp.route("/users/<int:id>", methods=["DELETE"])
@token_required
@role_required("admin")
def deletar_usuario(user_id, id):

    usuario = User.query.get(id)

    if not usuario:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404

    if usuario.id == user_id:
        return jsonify({
            "error": "Você não pode excluir o próprio usuário logado"
        }), 400

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário excluído com sucesso"
    }), 200


@user_bp.route("/users/<int:id>/toggle-access", methods=["PATCH"])
@token_required
@role_required("admin")
def toggle_access(user_id, id):

    usuario = User.query.get(id)

    if not usuario:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404

    if usuario.id == user_id:
        return jsonify({
            "error": "Você não pode bloquear seu próprio acesso"
        }), 400

    usuario.acesso_ativo = not usuario.acesso_ativo

    db.session.commit()

    return jsonify({
        "message": "Credencial atualizada com sucesso",
        "acesso_ativo": usuario.acesso_ativo
    }), 200