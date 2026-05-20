from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    acesso_ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.nome}>'