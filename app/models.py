from mongoengine import Document, StringField, ReferenceField, DateTimeField, EmailField
from flask_login import UserMixin
from datetime import datetime

class Regional(Document):
    nombre = StringField(required=True, unique=True)

class Programa(Document):
    nombre = StringField(required=True, unique=True)

class Instructor(UserMixin, Document):
    nombre = StringField(required=True)
    correo = EmailField(required=True, unique=True)
    regional = ReferenceField(Regional, required=True)
    password = StringField(required=True)

class GuiaAprendizaje(Document):
    nombre = StringField(required=True)
    descripcion = StringField()
    programa = ReferenceField(Programa, required=True)
    archivo = StringField(required=True)
    fecha = DateTimeField(default=datetime.now)
    instructor = ReferenceField(Instructor)
