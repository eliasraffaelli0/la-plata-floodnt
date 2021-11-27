from app.models.zone import Zone
import re


class ZoneValidator:
    def __init__(self, params, zone=None):
        self.errors = {}
        self.params = params
        self.zone = zone

    # Validaciones a efectuar a la hora de crear una zona
    def validate_create(self):
        self.__validate_name()
        self.__validate_input_field()

        return self.errors

    # Validaciones a efectuar a la hora de actualizar la info de una zona
    def validate_update(self):
        self.__validate_name_update()
        self.__validate_input_field()

        return self.errors

    def __validate_name(self):
        name_is_registered = Zone.query.filter(Zone.name == self.params.name).first()
        if name_is_registered:
            self.errors["name"] = "Ya existe una zona con este nombre"

    def __validate_input_field(self):
        if (
            self.params.name == ""
            or self.params.zone_code == ""
            or self.params.color == ""
        ):
            self.errors["emptyField"] = "Debe completar todos los campos"

    def __validate_name_update(self):
        name_is_registered = (
            Zone.query.filter(Zone.name == self.params.name)
            .filter(Zone.name != self.zone.name)
            .first()
        )

        if name_is_registered:
            self.errors["name"] = "Ya existe un punto con este nombre"
