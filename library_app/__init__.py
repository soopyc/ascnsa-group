import os
import uuid
from traceback import print_exception, format_exception
from datetime import datetime
from logging import basicConfig
from werkzeug.exceptions import HTTPException

from flask import Flask, g, render_template

from . import routes

basicConfig(
	format="[%(asctime)s %(levelname)s] (%(conn_id)s): %(message)s",
	level=os.environ.get("LOGGING", "debug").upper(),
)

app = Flask(__name__)
routes.register_routes(app)


@app.before_request
def proc_data():
	g.req_received = datetime.now()
	g.conn_id = str(uuid.uuid4())


@app.context_processor
def inject_data():
	return dict(
		connection_id=g.conn_id,
		processing_ms=round((datetime.now() - g.req_received).microseconds / 1000, 3),
	)


@app.errorhandler(Exception)
def handle_exception(e):
	# pass through HTTP errors
	if isinstance(e, HTTPException):
		return e

	print_exception(e)
	return render_template("error.html", error=''.join(format_exception(e)))
