from app import app
from flask import render_template
from flask_login import login_required
from app.models import User

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


