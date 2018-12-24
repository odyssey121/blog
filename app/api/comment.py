from flask import jsonify, g
from .. import db
from ..models import Comment

from . import api
from . errors import forbidden, bad_request


@api.route('/comments/<int:id>', methods = ['PUT'])
def approve_comment(id):
	comment = Comment.query.get_or_404(id)
	if comment.article.author != g.current_user and not g.current_user.is_admin:
		return forbidden('You cannot modify this comment.')
	#permission to approve
	if comment.approved:
		return bad_request('Comment is already approved.')
	comment.approved = True
	db.session.add(comment)
	db.session.commit()
	return jsonify({'status':'ok'})

<<<<<<< HEAD
@api.route('/comments/<int:id>', methods = ['DELETE'])
=======
@api.route('/comment/<int:id>', methods = ['DELETE'])
>>>>>>> 9c1d010460d3c6af320dd10439e5fb3051faeafa
def delete_comment(id):
	comment = Comment.query.get_or_404(id)
	if comment.article.author != g.current_user and not g.current_user.is_admin:
		return forbidden('You cannot modify this comment.')
	if comment.approved:
		return bad_request('Comment is already approved.')
	db.session.delete(comment)
	db.session.commit()
	return jsonify({'status':'ok'})
