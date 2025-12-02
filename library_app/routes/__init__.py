from flask import Flask

from . import root, books, borrowers, loans


def register_routes(app: Flask):
	app.register_blueprint(root.blueprint)
	app.register_blueprint(books.blueprint)
	app.register_blueprint(borrowers.blueprint)
	app.register_blueprint(loans.blueprint)
