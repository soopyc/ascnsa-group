from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
import pymysql

blueprint = Blueprint("borrowers", __name__, template_folder="../templates")

def get_conn():
    return pymysql.connect(
        host="127.0.0.1",
        user="user",
        password="userresu",
        database="library_app",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

@blueprint.get("/borrowers")
def list_borrowers():
    q = request.args.get("q")
    conn = get_conn()
    cur = conn.cursor()
    try:
        if q:
            cur.execute(
                """
                SELECT borrower_id, first_name, last_name, email, registration_date
                FROM Borrowers
                WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
                ORDER BY borrower_id ASC
                """,
                (f"%{q}%", f"%{q}%", f"%{q}%"),
            )
        else:
            cur.execute(
                """
                SELECT borrower_id, first_name, last_name, email, registration_date
                FROM Borrowers
                ORDER BY borrower_id ASC
                """
            )
        rows = cur.fetchall()
        return render_template("borrowers.html", borrowers=rows, q=q or "")
    finally:
        cur.close()
        conn.close()

@blueprint.get("/borrowers/new")
def new_borrower_form():
    return render_template("borrower_form.html", borrower=None)

@blueprint.post("/borrowers")
def create_borrower():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()

    if not first_name or not last_name or not email:
        return "Missing required fields", 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT MIN(t1.borrower_id + 1) AS next_id
            FROM Borrowers t1
            LEFT JOIN Borrowers t2 ON t1.borrower_id + 1 = t2.borrower_id
            WHERE t2.borrower_id IS NULL
        """)
        row = cur.fetchone()
        next_id = 1 if not row or not row["next_id"] else row["next_id"]

        cur.execute(
            """
            INSERT INTO Borrowers (borrower_id, first_name, last_name, email, registration_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (next_id, first_name, last_name, email, date.today()),
        )
        conn.commit()
        return redirect(url_for("borrowers.list_borrowers"))
    except pymysql.MySQLError as e:
        conn.rollback()
        return f"Insert failed: {e}", 400
    finally:
        cur.close()
        conn.close()


@blueprint.get("/borrowers/<int:borrower_id>/edit")
def edit_borrower_form(borrower_id: int):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT borrower_id, first_name, last_name, email, registration_date
            FROM Borrowers
            WHERE borrower_id = %s
            """,
            (borrower_id,),
        )
        row = cur.fetchone()
        if not row:
            return "Borrower not found", 404
        return render_template("borrower_form.html", borrower=row)
    finally:
        cur.close()
        conn.close()

@blueprint.post("/borrowers/<int:borrower_id>")
def update_borrower(borrower_id: int):
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()

    if not first_name or not last_name or not email:
        return "Missing required fields", 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE Borrowers
            SET first_name = %s, last_name = %s, email = %s
            WHERE borrower_id = %s
            """,
            (first_name, last_name, email, borrower_id),
        )
        conn.commit()
        return redirect(url_for("borrowers.list_borrowers"))
    except pymysql.MySQLError as e:
        conn.rollback()
        return f"Update failed: {e}", 400
    finally:
        cur.close()
        conn.close()

@blueprint.post("/borrowers/<int:borrower_id>/delete")
def delete_borrower(borrower_id: int):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Borrowers WHERE borrower_id = %s",
            (borrower_id,),
        )
        conn.commit()
        return redirect(url_for("borrowers.list_borrowers"))
    except pymysql.MySQLError as e:
        conn.rollback()
        return f"Delete failed: {e}", 400
    finally:
        cur.close()
        conn.close()
