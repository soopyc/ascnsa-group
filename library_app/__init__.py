from flask import Flask

from . import routes

app = Flask(__name__)
routes.register_routes(app)
