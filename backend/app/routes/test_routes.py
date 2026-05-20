from flask import Blueprint, jsonify
from app.utils.decorators import role_required

test_bp = Blueprint('test', __name__)

@test_bp.route('/admin-area', methods=['POST'])
@role_required(['admin'])
def admin_area():
    return jsonify({"message": "Bem-vindo à área de administrador"})