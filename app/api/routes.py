from flask import jsonify
from . import api
from .errors import bad_request
from app import db
from app.models import Comment


@api.route('/comments/<int:id>', methods = ['PUT'])
def approve_comment(id):
	comment = Comment.query.get_or_404(id)
	#permission to approve
	if comment.approved:
		return bad_request('Comment is already approved.')
	comment.approved = True
	db.session.add(comment)
	db.session.commit()
	return jsonify({'status':'ok'})

@api.route('/comment/<int:id>', methods = ['DELETE'])
def delete_comment(id):
	comment = Comment.query.get_or_404(id)
	db.session.remove(comment)
	db.session.commit()
