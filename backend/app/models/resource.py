from app.extensions import db

class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    localizacao = db.Column(db.String(100), nullable=True)
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Resource {self.nome}>'