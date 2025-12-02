from flask import Blueprint

blueprint = Blueprint('books', __name__)

@blueprint.route("/books")
def get():
	raise NotImplementedError()
