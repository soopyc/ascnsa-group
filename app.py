from flask import Flask

app = Flask("library_app")

@app.route("/")
def root():
	raise Exception("meow")

# TODO: make it routable with like a router thing or something
