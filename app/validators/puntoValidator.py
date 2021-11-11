from app.models.punto import Punto
import re


class PuntoValidator:
    def __init__(self, params, punto=None):
        self.errors = {}
        self.params = params
        self.punto = punto

    # Validaciones a efectuar a la hora de crear un usuario
    def validate_create(self):
        self.__validate_name()
        self.__validate_input_field()
        self.__validate_email_format()

        return self.errors

    # Validaciones a afectuar a la hora de actualizar la info de un usuario tercero
    def validate_update(self):
        self.__validate_email_format()
        self.__validate_name_update()
        self.__validate_input_field()

        return self.errors

    def __validate_email_format(self):
        # raw string utilizado para validar que se trate de un mail
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not (re.fullmatch(regex, self.params.email)):
            self.errors["email"] = "Ingrese un email válido"

    def __validate_name(self):
        name_is_registered = Punto.query.filter(Punto.name == self.params.name).first()
        if name_is_registered:
            self.errors["name"] = "Ya existe un punto con este nombre"

    def __validate_input_field(self):
        if (
            self.params.email == ""
            or self.params.name == ""
            or self.params.latitude == ""
            or self.params.longitude == ""
            or self.params.telephone == ""
        ):
            self.errors["emptyField"] = "Debe completar todos los campos"

    def __validate_name_update(self):
        name_is_registered = (
            Punto.query.filter(Punto.name == self.params.name)
            .filter(Punto.name != self.punto.name)
            .first()
        )

        if name_is_registered:
            self.errors["name"] = "Ya existe un punto con este nombre"
