from datetime import datetime

from flask import Flask, g

from . import routes

app = Flask(__name__)
routes.register_routes(app)


@app.before_request
def proc_start_time():
	g.req_received = datetime.now()


@app.context_processor
def inject_processing_time():
	return dict(
		processing_ms=round((datetime.now() - g.req_received).microseconds / 1000, 3)
	)
