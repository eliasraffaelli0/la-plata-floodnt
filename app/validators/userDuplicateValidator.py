from app.models.user import User
from flask import flash

def userDuplicateChecker(dbData, formData, dataType):
    user = User.query.filter(dbData == formData).first()
    if user:
        flash(f'El {dataType} ya está registrado.')
        return True