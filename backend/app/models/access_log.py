from app.extensions import db


class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey('areas.id'),
        nullable=False,
        index=True
    )

    status_acesso = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )

    motivo = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        index=True
    )

    usuario = db.relationship(
        'User',
        backref='access_logs',
        lazy=True
    )

    area = db.relationship(
        'Area',
        backref='access_logs',
        lazy=True
    )

    def __repr__(self):
        return f'<AccessLog User {self.user_id} - Area {self.area_id} - {self.status_acesso}>'