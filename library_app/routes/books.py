from flask import Blueprint, render_template, request, redirect, url_for
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
def books_list():
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("""
        SELECT b.book_id, b.title, b.isbn, b.book_type, b.status,
               GROUP_CONCAT(a.name SEPARATOR ', ') AS authors
        FROM Books b
        LEFT JOIN Book_Authors ba ON b.book_id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        GROUP BY b.book_id, b.title, b.isbn, b.book_type
        ORDER BY b.book_id ASC;
    """)
	rows = cursor.fetchall()
	cursor.close()
	conn.close()
	return render_template("books_list.html", books=rows)


@blueprint.route("/books/create", methods=["GET", "POST"])
def books_create():
	if request.method == "POST":
		title = request.form.get("title")
		isbn = request.form.get("isbn")
		author_name = request.form.get("author_name")

		conn = mysql.connector.connect(**DB_CONFIG)
		cursor = conn.cursor()
		try:
			# 1) create author
			cursor.execute("INSERT INTO Authors (name) VALUES (%s)", (author_name,))
			author_id = cursor.lastrowid

			# 2) create book
			cursor.execute(
				"""
                INSERT INTO Books (title, isbn, status, book_type)
                VALUES (%s, %s, 'available', 'Generic')
            """,
				(title, isbn),
			)
			book_id = cursor.lastrowid

			# 3) link
			cursor.execute(
				"""
                INSERT INTO Book_Authors (book_id, author_id)
                VALUES (%s, %s)
            """,
				(book_id, author_id),
			)

			conn.commit()
		finally:
			cursor.close()
			conn.close()

		return redirect(url_for("books.books_list"))

	return render_template("books_create.html")


@blueprint.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def books_edit(book_id):
	if request.method == "POST":
		title = request.form.get("title")
		isbn = request.form.get("isbn")
		book_type = request.form.get("book_type")
		author_name = request.form.get("author_name")

		conn = mysql.connector.connect(**DB_CONFIG)
		cursor = conn.cursor()

		# update book
		cursor.execute(
			"""
            UPDATE Books
            SET title = %s,
                isbn = %s,
                book_type = %s
            WHERE book_id = %s
        """,
			(title, isbn, book_type, book_id),
		)

		# update first linked author
		cursor.execute(
			"""
            UPDATE Authors
            SET name = %s
            WHERE author_id = (
                SELECT author_id FROM Book_Authors
                WHERE book_id = %s
                LIMIT 1
            )
        """,
			(author_name, book_id),
		)

		conn.commit()
		cursor.close()
		conn.close()
		return redirect(url_for("books.books_list"))

	# GET: load book + one author
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute(
		"""
        SELECT b.book_id, b.title, b.isbn, b.book_type,
               a.name AS author_name
        FROM Books b
        LEFT JOIN Book_Authors ba ON b.book_id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        WHERE b.book_id = %s
        LIMIT 1
    """,
		(book_id,),
	)
	book = cursor.fetchone()
	cursor.close()
	conn.close()

	return render_template("books_edit.html", book=book)


@blueprint.route("/books/<int:book_id>/delete", methods=["POST"])
def books_delete(book_id):
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor()

	# First remove links from Book_Authors
	cursor.execute("DELETE FROM Book_Authors WHERE book_id = %s", (book_id,))
	# Then delete the book itself
	cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))

	conn.commit()
	cursor.close()
	conn.close()
	return redirect(url_for("books.books_list"))
