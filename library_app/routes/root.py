from flask import render_template, Blueprint

blueprint = Blueprint('root', __name__)

@blueprint.get("/")
def get():
	return render_template("index.html")
