from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash({'title': "¡Genial!", 'message': "¡Inicio de sesión correcto!"}, 'success')
                login_user(user, remember=True)
                return redirect(url_for('notes.home'))
            else:
                flash({'title': "¡Error!", 'message': "Contraseña incorrecta, inténtalo de nuevo."}, 'error')
        else:
            flash({'title': "¡Error!", 'message': "El email no existe."}, 'error')
        
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signUp', methods=['GET', 'POST'])
def singUp():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash({'title': "¡Error!", 'message': "El email ya existe."}, 'error')
        elif len(nombres) < 2:
            flash({'title': "¡Error!", 'message': "Los nombres deben tener más de 1 carácter."}, 'error')
        elif len(apellidos) < 2:
            flash({'title': "¡Error!", 'message': "Los apellidos deben tener más de 1 carácter."}, 'error')
        elif len(email) < 4:
            flash({'title': "¡Error!", 'message': "El correo electrónico debe tener más de 3 caracteres."}, 'error')
        elif password1 != password2:
            flash({'title': "¡Error!", 'message': "Las contraseñas no coinciden."}, 'error')
        elif len(password1) < 7:
            flash({'title': "¡Error!", 'message': "La contraseña debe tener al menos 7 caracteres."}, 'error')
        else:
            new_user = User(nombres=nombres, apellidos=apellidos, email=email, 
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash({'title': "¡Genial!", 'message': "¡La cuenta ha sido creada!"}, 'success')
            return redirect(url_for('notes.home'))
        
    return render_template('signUp.html', user=current_user)