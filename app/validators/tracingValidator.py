from app.models.tracing import Tracing
import re


class TracingValidator:
    def __init__(self, params, tracing=None):
        self.errors = {}
        self.params = params
        self.tracing = tracing

    # Validaciones a efectuar a la hora de crear un seguimiento
    def validate_create(self):
        self.__validate_input_field()

        return self.errors

    def __validate_input_field(self):
        if self.params.description == "":
            self.errors["emptyField"] = "Debe completar todos los campos"
