from flask import Flask
from app.extensions import db, login_manager,mail

def create_app():
    app = Flask(__name__, template_folder="templates")

    #Configuración
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brief.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from app.models import User, Project, BriefResponse

    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.routes.campo_routes import campo_bp
    from app.routes.data_routes import data_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(campo_bp)
    app.register_blueprint(data_bp)  

    mail.init_app(app)
    
    return app




