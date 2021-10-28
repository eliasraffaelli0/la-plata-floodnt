from app.models.user import User
import re


class UserValidator:
    def __init__(self, user, params):
        self.errors = {}
        self.user = user

    def validate(self):
        self.__validate_username()
        self.__validate_email_format()
        self.__validate_email()
        self.__validate_input_field()

        return self.errors

    def __validate_email_format(self):
        # raw string utilizado para validar que se trate de un mail
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not (re.fullmatch(regex, self.user.email)):
            self.errors["email"] = "Ya existe un usuario con este email"

    def __validate_email(self):
        mail_is_registered = User.query.filter(User.email == self.user.email).first()
        if mail_is_registered:
            self.errors["email"] = "Ya existe un usuario con este email"

    def __validate_username(self):
        username_is_registered = User.query.filter(
            User.username == self.user.username
        ).first()
        if username_is_registered:
            self.errors["username"] = "Ya existe un usuario con este username"

    def __validate_input_field(self):
        if (
            self.user.email == ""
            or self.user.username == ""
            or self.user.password == ""
            or self.user.first_name == ""
            or self.user.last_name == ""
        ):
            self.errors["emptyField"] = "Debe completar todos los campos"
