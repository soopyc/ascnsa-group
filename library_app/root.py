from flask import render_template

from . import app

@app.get("/")
def get():
	return render_template("index.html")
