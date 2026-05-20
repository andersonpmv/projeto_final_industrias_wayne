from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.area import Area

app = create_app()

with app.app_context():
    Area.query.delete()
    User.query.delete()

    usuarios = [
        User(
            nome="Bruce Wayne",
            email="admin@wayne.com",
            senha=bcrypt.generate_password_hash("123456").decode("utf-8"),
            cargo="admin"
        ),
        User(
            nome="Lucius Fox",
            email="gerente@wayne.com",
            senha=bcrypt.generate_password_hash("123456").decode("utf-8"),
            cargo="gerente"
        ),
        User(
            nome="Dick Grayson",
            email="funcionario@wayne.com",
            senha=bcrypt.generate_password_hash("123456").decode("utf-8"),
            cargo="funcionario"
        )
    ]

    areas = [
        Area(
            nome="Batcaverna",
            nivel_restricao=3,
            descricao="Área de operações estratégicas"
        ),
        Area(
            nome="Laboratório P&D",
            nivel_restricao=2,
            descricao="Pesquisa e desenvolvimento"
        ),
        Area(
            nome="Recepção",
            nivel_restricao=1,
            descricao="Área de acesso básico"
        )
    ]

    db.session.add_all(usuarios)
    db.session.add_all(areas)
    db.session.commit()

    print("Usuários e áreas criados com sucesso!")