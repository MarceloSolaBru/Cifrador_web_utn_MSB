from flask import Flask 
from flask_marshmallow import (Marshmallow,)
import os  
from flask_migrate import (Migrate,)  
from flask_sqlalchemy import (SQLAlchemy,)  
from app.config import (config,)  
from flask_login import LoginManager

# Crea instancias de las extensiones
db = SQLAlchemy()  # Instancia de SQLAlchemy para interactuar con la base de datos
migrate = Migrate()  # Instancia de Flask-Migrate para migraciones de base de datos
ma = Marshmallow()  # Instancia de Marshmallow para la serialización y deserialización de objetos
login_manager = LoginManager()

# Define una función para crear la aplicación Flask
def create_app() -> Flask:

    from app import db

    # Obtiene el contexto de la aplicación desde la variable de entorno FLASK_CONTEXT
    app_context = os.getenv("FLASK_CONTEXT")

    # Crea una instancia de la aplicación Flask
    app = Flask(__name__)  

    # Obtiene la configuración correspondiente al contexto de la aplicación (desarrollo, producción, etc.)
    config_instance = config.factory(app_context if app_context else "development")
    app.config.from_object(config_instance)  # Configura la aplicación con la instancia de configuración obtenida

    # Inicializa las extensiones con la aplicación
    ma.init_app(app)  
    db.init_app(app)  
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)  # Inicializa Flask-Migrate con la aplicación y la instancia de SQLAlchemy

    # # Registra los blueprints (enrutadores modulares) en la aplicación
    # from app.auth.routes import auth as auth_blueprint
    # from app.routes import index as index_blueprint
    # from app.resources import home as home_blueprint



    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}
    
    return app  # Retorna la aplicación Flask creada
