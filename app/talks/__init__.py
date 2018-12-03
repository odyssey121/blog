from flask import Blueprint

bp = Blueprint('talks', __name__)

from app.talks import routes
