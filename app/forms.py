from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed
from .models import Regional, Programa

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    regional = SelectField('Regional', choices=[], coerce=str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regional.choices = [(str(r.id), r.nombre) for r in Regional.objects()]

class GuiaForm(FlaskForm):
    nombre = StringField('Nombre Guía', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    programa = SelectField('Programa', choices=[], coerce=str)
    archivo = FileField('Archivo PDF', validators=[DataRequired(), FileAllowed(['pdf'], 'PDFs solamente')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.programa.choices = [(str(p.id), p.nombre) for p in Programa.objects()]
