from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.resource import Resource
from app.utils.auth_decorators import token_required
from app.utils.role_decorator import role_required

resource_bp = Blueprint('resource', __name__)

@resource_bp.route('/resources', methods=['GET'])
def listar_recursos():
    recursos = Resource.query.all()

    resultado = []
    for recurso in recursos:
        resultado.append({
            "id": recurso.id,
            "nome": recurso.nome,
            "categoria": recurso.categoria,
            "status": recurso.status,
            "localizacao": recurso.localizacao,
            "descricao": recurso.descricao
        })

    return jsonify(resultado), 200


@resource_bp.route('/resources', methods=['POST'])
@token_required
@role_required('admin', 'gerente')
def criar_recurso(user_id):
    data = request.get_json()

    nome = data.get('nome')
    categoria = data.get('categoria')
    status = data.get('status')
    localizacao = data.get('localizacao')
    descricao = data.get('descricao')

    if not nome or not categoria or not status:
        return jsonify({"error": "nome, categoria e status são obrigatórios"}), 400

    categorias_validas = ['equipamento', 'veiculo', 'dispositivo_seguranca']
    status_validos = ['ativo', 'manutencao', 'inativo']

    if categoria not in categorias_validas:
        return jsonify({"error": "categoria inválida"}), 400

    if status not in status_validos:
        return jsonify({"error": "status inválido"}), 400

    novo_recurso = Resource(
        nome=nome,
        categoria=categoria,
        status=status,
        localizacao=localizacao,
        descricao=descricao
    )

    db.session.add(novo_recurso)
    db.session.commit()

    return jsonify({"message": "Recurso criado com sucesso"}), 201


@resource_bp.route('/resources/<int:id>', methods=['PUT'])
@token_required
@role_required('admin', 'gerente')
def atualizar_recurso(user_id, id):
    recurso = Resource.query.get(id)

    if not recurso:
        return jsonify({"error": "Recurso não encontrado"}), 404

    data = request.get_json()

    categoria = data.get('categoria', recurso.categoria)
    status = data.get('status', recurso.status)

    categorias_validas = ['equipamento', 'veiculo', 'dispositivo_seguranca']
    status_validos = ['ativo', 'manutencao', 'inativo']

    if categoria not in categorias_validas:
        return jsonify({"error": "categoria inválida"}), 400

    if status not in status_validos:
        return jsonify({"error": "status inválido"}), 400

    recurso.nome = data.get('nome', recurso.nome)
    recurso.categoria = categoria
    recurso.status = status
    recurso.localizacao = data.get('localizacao', recurso.localizacao)
    recurso.descricao = data.get('descricao', recurso.descricao)

    db.session.commit()

    return jsonify({"message": "Recurso atualizado com sucesso"}), 200


@resource_bp.route('/resources/<int:id>', methods=['DELETE'])
@token_required
@role_required('admin')
def deletar_recurso(user_id, id):
    recurso = Resource.query.get(id)

    if not recurso:
        return jsonify({"error": "Recurso não encontrado"}), 404

    db.session.delete(recurso)
    db.session.commit()

    return jsonify({"message": "Recurso excluído com sucesso"}), 200