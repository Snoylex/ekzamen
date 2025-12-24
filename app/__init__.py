import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager

mysql = MySQL()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы оставить отзыв.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object('config.Config')

    mysql.init_app(app)
    login_manager.init_app(app)

    from .routes import main_bp, auth_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)  # Регистрация админки

    from .models import load_user
    login_manager.user_loader(load_user)

    app.jinja_env.filters['nl2br'] = lambda value: value.replace('\n', '<br>') if value else ''

    return app