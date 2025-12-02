from flask import Blueprint

blueprint = Blueprint("loans", __name__)


@blueprint.route("/loans")
def handle():
	raise NotImplementedError()
