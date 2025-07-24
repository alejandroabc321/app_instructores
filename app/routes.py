from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from .forms import RegistroForm, GuiaForm
from .models import Instructor, GuiaAprendizaje
from . import mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import login_manager
import os
import uuid

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Instructor.objects(pk=user_id).first()

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        user = Instructor.objects(correo=correo).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.subir_guia'))
        flash("Credenciales incorrectas.")
    return render_template('login.html')

import random
import string

def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if Instructor.objects(correo=form.correo.data).first():
            flash("Correo ya registrado.")
            return redirect(url_for('main.registro'))
        


        from .models import Regional
        regional_obj = Regional.objects(id=form.regional.data).first()

        password = generar_password()
        hashed_pw = generate_password_hash(password)

        nuevo = Instructor(
            nombre=form.nombre.data,
            correo=form.correo.data,
            regional=regional_obj,
            password=hashed_pw
        )
        nuevo.save()
        print(f"Nuevo usuario registrado: {nuevo.nombre} con correo {nuevo.correo}")

        # Enviar correo
        msg = Message("Credenciales de acceso - Plataforma SENA",
                      recipients=[form.correo.data])
        msg.body = f"""Hola {form.nombre.data},
Tu usuario ha sido registrado exitosamente.

Correo: {form.correo.data}
Contraseña: {password}

Accede desde: http://localhost:5000/
"""
        mail.send(msg)

        flash("Registro exitoso. Se enviaron las credenciales al correo.")
        return redirect(url_for('main.login'))

    return render_template('registro.html', form=form)


@main.route('/subir', methods=['GET', 'POST'])
@login_required
def subir_guia():
    form = GuiaForm()
    if form.validate_on_submit():
        archivo = form.archivo.data
        filename = f"{uuid.uuid4().hex}.pdf"
        path = os.path.join('uploads', filename)
        archivo.save(path)

        from .models import Programa
        programa_obj = Programa.objects(id=form.programa.data).first()

        guia = GuiaAprendizaje(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            programa=programa_obj,
            archivo=filename,
            instructor=current_user._get_current_object()
        )
        guia.save()
        flash("Guía subida exitosamente.")
        return redirect(url_for('main.listar_guias'))
    return render_template('subir_guia.html', form=form)


@main.route('/listar')
@login_required
def listar_guias():
    guias = GuiaAprendizaje.objects()
    return render_template('listar_guias.html', guias=guias)


@main.route('/ver_pdf/<filename>')
@login_required
def ver_pdf(filename):
    import os
    uploads_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'uploads')
    return send_from_directory(uploads_path, filename)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


