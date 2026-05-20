from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.area import Area
from app.utils.auth_decorators import token_required
from app.utils.role_decorator import role_required

area_bp = Blueprint('area', __name__)

@area_bp.route('/areas', methods=['GET'])
def listar_areas():
    areas = Area.query.all()

    resultado = []
    for area in areas:
        resultado.append({
            "id": area.id,
            "nome": area.nome,
            "nivel_restricao": area.nivel_restricao,
            "descricao": area.descricao
        })

    return jsonify(resultado), 200


@area_bp.route('/areas', methods=['POST'])
@token_required
@role_required('admin')
def criar_area(user_id):
    data = request.get_json()

    nome = data.get('nome')
    nivel_restricao = data.get('nivel_restricao')
    descricao = data.get('descricao')

    if not nome or not nivel_restricao:
        return jsonify({"error": "nome e nivel_restricao são obrigatórios"}), 400

    if nivel_restricao not in [1, 2, 3]:
        return jsonify({"error": "nivel_restricao deve ser 1, 2 ou 3"}), 400

    nova_area = Area(
        nome=nome,
        nivel_restricao=nivel_restricao,
        descricao=descricao
    )

    db.session.add(nova_area)
    db.session.commit()

    return jsonify({"message": "Área criada com sucesso"}), 201