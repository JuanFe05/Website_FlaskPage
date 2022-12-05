from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_required
from flask_fontawesome import FontAwesome
from flask_toastr import Toastr

db = SQLAlchemy()
DB_NAME = "flask_project"

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    fa = FontAwesome(app)
    toastr = Toastr(app)
    
    app.register_error_handler(404, page_not_found)
    
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:@localhost/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    from .routes.notes import notes
    from .routes.auth import auth
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(notes, url_prefix='/')
    
    from .models.models import User, Note
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('¡Base de datos creada!')