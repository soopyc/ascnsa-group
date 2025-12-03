from flask import Blueprint, render_template
import mysql.connector

blueprint = Blueprint("books", __name__)

DB_CONFIG = {
	"host": "127.0.0.1", 
    "user": "user",
    "password": "userresu",
    "database": "library_app",
	"port": 3306,
}

@blueprint.route("/books")
def handle():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    html = "<h1>Books</h1><table border=1>"
    html += "<p><a href='/books/create'><button>Create New Book</button></a></p>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{v}</td>" for v in row.values()) + "</tr>"
    html += "</table>"
    
    return html

@blueprint.route("/books/create")
def handle2():
    raise NotImplementedError()
