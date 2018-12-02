from app.errors import bp
from flask import render_template
from app import db

@bp.app_errorhandler(404)
def not_fount_error(error):
	return render_template('errors/404.html'), 404

# #internal error 
# @bp.app_errorhandler(500)
# def internal_error(error):
# 	db.session.rollback()
# 	return render_template('errors/500.html'), 500