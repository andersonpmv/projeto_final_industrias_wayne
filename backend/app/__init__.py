from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # IMPORTA E REGISTRA ROTAS AQUI
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.test_routes import test_bp
    app.register_blueprint(test_bp)

    from app.routes.resource_routes import resource_bp
    app.register_blueprint(resource_bp)

    from app.routes.area_routes import area_bp
    app.register_blueprint(area_bp)

    from app.routes.access_routes import access_bp
    app.register_blueprint(access_bp)

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    with app.app_context():
        from app.models import User, Area, Resource, AccessLog
        db.create_all()

    @app.route('/')
    def home():
        return {"message": "Wayne Security System Online"}

    return app