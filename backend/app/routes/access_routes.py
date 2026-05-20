from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.area import Area
from app.models.access_log import AccessLog
from app.utils.auth_decorators import token_required
from app.utils.role_decorator import role_required

access_bp = Blueprint('access', __name__)


@access_bp.route('/access/check', methods=['POST'])
@token_required
def verificar_acesso(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Body JSON é obrigatório"}), 400

    area_id = data.get('area_id')

    if not area_id:
        return jsonify({"error": "area_id é obrigatório"}), 400

    user = User.query.get(user_id)
    area = Area.query.get(area_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not area:
        return jsonify({"error": "Área não encontrada"}), 404

    if not user.ativo:
        log = AccessLog(
            user_id=user.id,
            area_id=area.id,
            status_acesso="negado",
            motivo="Usuário inativo"
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "message": "Acesso negado",
            "status_acesso": "negado",
            "usuario": user.nome,
            "area": area.nome,
            "motivo": "Usuário inativo"
        }), 403

    if not user.acesso_ativo:
        log = AccessLog(
            user_id=user.id,
            area_id=area.id,
            status_acesso="negado",
            motivo="Acesso revogado pelo administrador"
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "message": "Acesso negado",
            "status_acesso": "negado",
            "usuario": user.nome,
            "area": area.nome,
            "motivo": "Acesso revogado pelo administrador"
        }), 403

    cargo_niveis = {
        "funcionario": 1,
        "gerente": 2,
        "admin": 3
    }

    nivel_usuario = cargo_niveis.get(user.cargo, 0)

    if nivel_usuario >= area.nivel_restricao:
        status_acesso = "permitido"
        motivo = "Acesso autorizado"
        mensagem = "Acesso permitido"
        status_http = 200
    else:
        status_acesso = "negado"
        motivo = "Nível de acesso insuficiente"
        mensagem = "Acesso negado"
        status_http = 403

    log = AccessLog(
        user_id=user.id,
        area_id=area.id,
        status_acesso=status_acesso,
        motivo=motivo
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": mensagem,
        "status_acesso": status_acesso,
        "usuario": user.nome,
        "area": area.nome,
        "motivo": motivo
    }), status_http


@access_bp.route('/access/logs', methods=['GET'])
@token_required
@role_required('admin', 'gerente')
def listar_logs(user_id):
    usuario_id = request.args.get('user_id', type=int)
    area_id = request.args.get('area_id', type=int)
    status = request.args.get('status')

    query = db.session.query(
        AccessLog,
        User.nome.label("usuario_nome"),
        Area.nome.label("area_nome")
    ).join(
        User,
        AccessLog.user_id == User.id
    ).join(
        Area,
        AccessLog.area_id == Area.id
    )

    if usuario_id:
        query = query.filter(AccessLog.user_id == usuario_id)

    if area_id:
        query = query.filter(AccessLog.area_id == area_id)

    if status:
        query = query.filter(AccessLog.status_acesso == status)

    logs = query.order_by(AccessLog.id.desc()).all()

    resultado = []

    for log, usuario_nome, area_nome in logs:
        resultado.append({
            "id": log.id,
            "user_id": log.user_id,
            "usuario": usuario_nome,
            "area_id": log.area_id,
            "area": area_nome,
            "status_acesso": log.status_acesso,
            "motivo": log.motivo,
            "created_at": log.created_at.strftime('%Y-%m-%d %H:%M:%S') if log.created_at else None
        })

    return jsonify(resultado), 200