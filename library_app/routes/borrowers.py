from flask import Blueprint

blueprint = Blueprint("borrowers", __name__)


@blueprint.route("/borrowers")
def handle():
	raise NotImplementedError()
