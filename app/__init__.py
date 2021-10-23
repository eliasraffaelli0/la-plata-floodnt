from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import user
from app.resources import auth
from app.resources import puntos
from app.resources import recorridos
from app.resources import zonas
# from app.resources.api.issue import issue_api
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import permisoValidator as helper_permisos
import logging

#Sentencias que muestran el log de las querys que ejecuta la aplicación

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)




def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    conf = config[env]
    app.config.from_object(conf)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_permisos.permisoChecker)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/edit", "user_edit", user.new)

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de Zonas inundables
    app.add_url_rule("/zonas_inundables", "zonas_index", zonas.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)

    # Rutas de Puntos de encuentro
    app.add_url_rule("/puntos_de_encuentro", "puntos_index", puntos.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)

    # Rutas de Recorridos de evacuación
    app.add_url_rule("/recorridos_de_evacuacion", "recorridos_index", recorridos.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)

    # # Rutas de API-REST (usando Blueprints)
    # api = Blueprint("api", __name__, url_prefix="/api")
    # api.register_blueprint(issue_api)

    # app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
