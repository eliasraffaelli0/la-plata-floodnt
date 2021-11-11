from app.models.user import User
import re


class UserValidator:
    def __init__(self, params, user=None):
        self.errors = {}
        self.params = params
        self.user = user

    # Validaciones a efectuar a la hora de crear un usuario
    def validate_create(self):
        self.__validate_email_format()
        self.__validate_email()
        self.__validate_username()
        self.__validate_input_field()

        return self.errors

    # Validaciones a afectuear a la hora de actualizar la info de un usuario tercero
    def validate_update(self):
        self.__validate_email_format()
        self.__validate_email_update()
        self.__validate_username_update()
        self.__validate_input_field()

        return self.errors

    def __validate_email_format(self):
        # raw string utilizado para validar que se trate de un mail
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not (re.fullmatch(regex, self.params.email)):
            self.errors["email"] = "Ingrese un email válido"

    def __validate_email(self):
        mail_is_registered = User.query.filter(User.email == self.params.email).first()
        if mail_is_registered:
            self.errors["email"] = "Ya existe un usuario con este email"

    def __validate_username(self):
        username_is_registered = User.query.filter(
            User.username == self.params.username
        ).first()
        if username_is_registered:
            self.errors["username"] = "Ya existe un usuario con este username"

    def __validate_input_field(self):
        if (
            self.params.email == ""
            or self.params.username == ""
            or self.params.password == ""
            or self.params.first_name == ""
            or self.params.last_name == ""
        ):
            self.errors["emptyField"] = "Debe completar todos los campos"

    def __validate_email_update(self):
        mail_is_registered = (
            User.query.filter(User.email == self.params.email)
            .filter(User.email != self.user.email)
            .first()
        )

        if mail_is_registered:
            self.errors["email"] = "Ya existe un usuario con este email"

    def __validate_username_update(self):
        mail_is_registered = (
            User.query.filter(User.username == self.params.username)
            .filter(User.username != self.user.username)
            .first()
        )
        if mail_is_registered:
            self.errors["username"] = "Ya existe un usuario con este username"
