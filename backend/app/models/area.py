from app.extensions import db

class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    nivel_restricao = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Area {self.nome}>'