from app.models.report import Report
import re


class ReportValidator:
    def __init__(self, params, report=None):
        self.errors = {}
        self.params = params
        self.report = report

    # Validaciones a efectuar a la hora de crear un usuario
    def validate_create(self):
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
        if not (re.fullmatch(regex, self.params.complainant_email)):
            self.errors["email"] = "Ingrese un email válido"

    def __validate_input_field(self):
        if (
            self.params.title == ""
            or self.params.description == ""
            or self.params.latitude == ""
            or self.params.longitude == ""
            or self.params.complainant_telephone == ""
            or self.params.complainant_email == ""
            or self.params.complainant_name == ""
            or self.params.complainant_last_name == ""
        ):
            self.errors["emptyField"] = "Debe completar todos los campos"
