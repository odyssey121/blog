from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix = '/auth')


from app import routes

