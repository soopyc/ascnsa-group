from flask import Flask

from . import root, books


def register_routes(app: Flask):
	app.register_blueprint(root.blueprint)
	app.register_blueprint(books.blueprint)
