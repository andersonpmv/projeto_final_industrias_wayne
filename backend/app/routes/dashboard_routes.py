from flask import Blueprint, jsonify
from sqlalchemy import func

from app.extensions import db
from app.models.access_log import AccessLog
from app.models.user import User
from app.models.area import Area
from app.models.resource import Resource
from app.utils.auth_decorators import token_required
from app.utils.role_decorator import role_required


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard/summary', methods=['GET'])
@token_required
@role_required('admin', 'gerente', 'funcionario')
def dashboard_summary(user_id):

    total_logs = db.session.query(func.count(AccessLog.id)).scalar()

    total_permitidos = db.session.query(func.count(AccessLog.id)).filter(
        AccessLog.status_acesso == 'permitido'
    ).scalar()

    total_negados = db.session.query(func.count(AccessLog.id)).filter(
        AccessLog.status_acesso == 'negado'
    ).scalar()

    total_usuarios = db.session.query(func.count(User.id)).scalar()

    usuarios_ativos = db.session.query(func.count(User.id)).filter(
        User.acesso_ativo == True
    ).scalar()

    usuarios_bloqueados = db.session.query(func.count(User.id)).filter(
        User.acesso_ativo == False
    ).scalar()

    total_areas = db.session.query(func.count(Area.id)).scalar()

    total_recursos = db.session.query(func.count(Resource.id)).scalar()

    por_status_query = db.session.query(
        AccessLog.status_acesso,
        func.count(AccessLog.id)
    ).group_by(
        AccessLog.status_acesso
    ).all()

    por_status = {
        status: quantidade
        for status, quantidade in por_status_query
    }

    acessos_por_area_query = db.session.query(
        Area.nome,
        func.count(AccessLog.id)
    ).join(
        AccessLog,
        AccessLog.area_id == Area.id
    ).group_by(
        Area.nome
    ).all()

    acessos_por_area = [
        {
            "area": nome,
            "quantidade": quantidade
        }
        for nome, quantidade in acessos_por_area_query
    ]

    area_mais_acessada = None

    if acessos_por_area_query:

        nome_area, quantidade = max(
            acessos_por_area_query,
            key=lambda item: item[1]
        )

        area_mais_acessada = {
            "nome": nome_area,
            "quantidade": quantidade
        }

    usuario_com_mais_negados_query = db.session.query(
        User.nome,
        func.count(AccessLog.id)
    ).join(
        AccessLog,
        AccessLog.user_id == User.id
    ).filter(
        AccessLog.status_acesso == 'negado'
    ).group_by(
        User.nome
    ).order_by(
        func.count(AccessLog.id).desc()
    ).first()

    usuario_com_mais_negados = None

    if usuario_com_mais_negados_query:

        nome_usuario, quantidade = usuario_com_mais_negados_query

        usuario_com_mais_negados = {
            "nome": nome_usuario,
            "quantidade": quantidade
        }

    return jsonify({
        "total_logs": total_logs,
        "total_permitidos": total_permitidos,
        "total_negados": total_negados,
        "total_usuarios": total_usuarios,
        "usuarios_ativos": usuarios_ativos,
        "usuarios_bloqueados": usuarios_bloqueados,
        "total_areas": total_areas,
        "total_recursos": total_recursos,
        "por_status": por_status,
        "area_mais_acessada": area_mais_acessada,
        "usuario_com_mais_negados": usuario_com_mais_negados,
        "acessos_por_area": acessos_por_area
    }), 200


@dashboard_bp.route('/dashboard/security-alerts', methods=['GET'])
@token_required
@role_required('admin', 'gerente', 'funcionario')
def dashboard_security_alerts(user_id):

    negados_por_usuario_query = db.session.query(
        User.nome,
        func.count(AccessLog.id).label("negados")
    ).join(
        AccessLog,
        AccessLog.user_id == User.id
    ).filter(
        AccessLog.status_acesso == 'negado'
    ).group_by(
        User.id,
        User.nome
    ).all()

    total_por_usuario_query = db.session.query(
        User.nome,
        func.count(AccessLog.id).label("total")
    ).join(
        AccessLog,
        AccessLog.user_id == User.id
    ).group_by(
        User.id,
        User.nome
    ).all()

    total_por_usuario = {
        nome: total
        for nome, total in total_por_usuario_query
    }

    usuarios_suspeitos = []

    for nome, quantidade_negados in negados_por_usuario_query:

        total_tentativas = total_por_usuario.get(nome, 0)

        if total_tentativas == 0:
            continue

        taxa_negacao = round(
            (quantidade_negados / total_tentativas) * 100,
            2
        )

        if total_tentativas >= 3 and (
            quantidade_negados >= 3 or taxa_negacao >= 70
        ):

            usuarios_suspeitos.append({
                "nome": nome,
                "negados": quantidade_negados,
                "total_tentativas": total_tentativas,
                "taxa_negacao": taxa_negacao
            })

    negados_por_area_query = db.session.query(
        Area.nome,
        func.count(AccessLog.id).label("negados")
    ).join(
        AccessLog,
        AccessLog.area_id == Area.id
    ).filter(
        AccessLog.status_acesso == 'negado'
    ).group_by(
        Area.id,
        Area.nome
    ).all()

    areas_sensiveis = []

    for nome_area, quantidade_negados in negados_por_area_query:

        if quantidade_negados >= 2:

            areas_sensiveis.append({
                "area": nome_area,
                "negados": quantidade_negados
            })

    usuarios_suspeitos.sort(
        key=lambda item: item["negados"],
        reverse=True
    )

    areas_sensiveis.sort(
        key=lambda item: item["negados"],
        reverse=True
    )

    return jsonify({
        "usuarios_suspeitos": usuarios_suspeitos,
        "areas_sensiveis": areas_sensiveis
    }), 200