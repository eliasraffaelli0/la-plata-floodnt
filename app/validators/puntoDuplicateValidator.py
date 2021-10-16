from app.models.punto import Punto
from flask import flash

def puntoDuplicateChecker(dbData, formData, dataType):
    punto = Punto.query.filter(dbData == formData).first()
    if punto:
        if dataType=='coordenadas':
            flash (f'Las {dataType} ya están registradas')
        else:    
            flash(f'El {dataType} ya está registrado.')
        return True