from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from flask_cors import CORS
from app import resources
from config import config
from app import db
from app.resources import (
    evacuationRoute,
    user,
    auth,
    punto,
    zones,
    configuracion,
    report,
)
from app.models.configuracion import Configuracion
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import permisoValidator as helper_permisos
from app.resources.api.point import point_api


# import logging
# Sentencias que muestran el log de las querys que ejecuta la aplicación

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    CORS(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    conf = config[env]
    app.config.from_object(conf)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    # app.config["SQLALCHEMY_ECHO"] = environment == "development"
    # db.init_app(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{app.config['DB_USER']}:{app.config['DB_PASS']}@{app.config['DB_HOST']}:3306/{app.config['DB_NAME']}"
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_permisos.permisoChecker)

    # Autenticación
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios/nuevo", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule(
        "/usuarios/<string:username>",
        "user_edit_estado",
        user.update_estado,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/usuarios/edit/<int:id>",
        "user_edit",
        user.editInfo,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/usuarios/edit/<int:id>/info",
        "user_edit_info",
        user.edit,
        methods=["GET"],
    )
    app.add_url_rule(
        "/usuarios/edit/<int:id>/rol",
        "user_edit_rol",
        user.editRol,
        methods=["GET", "POST"],
    )

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        c = Configuracion.query.first()
        g.config = c
        return render_template("home.html")

    # Rutas de Zonas inundables
    app.add_url_rule("/flood_zones", "zones_index", zones.index)
    app.add_url_rule(
        "/flood_zones", "zonas_upload", zones.upload_file, methods=["POST"]
    )
    app.add_url_rule("/flood_zones/new", "zones_new", zones.new)
    app.add_url_rule("/flood_zones/new", "zones_create", zones.create, methods=["POST"])
    app.add_url_rule("/flood_zones/<int:id>", "zones_delete", zones.delete)
    app.add_url_rule(
        "/flood_zones/edit/<int:id>",
        "zones_edit",
        zones.edit,
        methods=["GET"],
    )
    app.add_url_rule(
        "/flood_zones/edit/<int:id>",
        "zones_edit_info",
        zones.editInfo,
        methods=["GET", "POST"],
    )
    # Rutas de Puntos de encuentro
    app.add_url_rule("/puntos_de_encuentro", "puntos_index", punto.index)
    app.add_url_rule(
        "/puntos_de_encuentro/nuevo", "puntos_create", punto.create, methods=["POST"]
    )
    app.add_url_rule("/puntos_de_encuentro/nuevo", "puntos_new", punto.new)
    app.add_url_rule(
        "/puntos_de_encuentro/edit/<int:id>",
        "puntos_edit",
        punto.edit,
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntos_de_encuentro/edit/<int:id>",
        "puntos_edit_info",
        punto.editInfo,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/puntos_de_encuentro/<int:id>", "puntos_delete", punto.delete)

    # Rutas de Recorridos de evacuación
    app.add_url_rule("/evacuationRoute", "evacuationRoute_index", evacuationRoute.index)
    app.add_url_rule(
        "/evacuationRoute/nuevo",
        "evacuationRoute_create",
        evacuationRoute.create,
        methods=["POST"],
    )
    app.add_url_rule(
        "/evacuationRoute/nuevo", "evacuationRoute_new", evacuationRoute.new
    )
    app.add_url_rule(
        "/evacuationRoute/edit/<int:id>",
        "evacuationRoute_edit",
        evacuationRoute.edit,
        methods=["GET"],
    )
    app.add_url_rule(
        "/evacuationRoute/edit/<int:id>",
        "evacuationRoute_edit_info",
        evacuationRoute.editInfo,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/evacuationRoute/<int:id>", "evacuationRoute_delete", evacuationRoute.delete
    )

    # Rutas del Modulo de Denuncias

    app.add_url_rule("/reports", "reports_index", report.index)
    app.add_url_rule("/reports/new", "reports_new", report.new)
    app.add_url_rule(
        "/reports/new",
        "reports_create",
        report.create,
        methods=["POST"],
    )
    # Rutas del Modulo de Configuración
    app.add_url_rule("/configuracion", "configuracion_index", configuracion.index)
    app.add_url_rule(
        "/configuracion", "configuracion_update", configuracion.update, methods=["POST"]
    )

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(point_api)

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Seteo la configuracion antes de todos los request
    @app.before_request
    def set_configuration():
        config = Configuracion.query.first()
        g.config = config

    # Retornar la instancia de app configurada
    return app
