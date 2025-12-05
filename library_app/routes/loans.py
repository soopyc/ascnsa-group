from flask import Blueprint, render_template, request, redirect

from library_app import db


blueprint = Blueprint("loans", __name__)


# show loans details
@blueprint.route("/loans")
def show_loans():
	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute("SELECT * FROM Loans")  # get all from Loans table
			rows = cursor.fetchall()
			return render_template("loans.html", loans=rows)


# craete new loans
@blueprint.route("/loans/create", methods=["GET", "POST"])
def create_loans():
	if request.method == "GET":
		return render_template("create_loan.html")
	book_id = int(request.form.get("book_id"))
	borrower_id = int(request.form.get("borrower_id"))
	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute(
				"INSERT INTO Loans (book_id,borrower_id,loan_date,due_date,return_date) VALUES (%s,%s,CURDATE(), CURDATE() + 14, NULL)",
				(book_id, borrower_id),
			)
			conn.commit()
			return redirect("/loans")


# show the edit loans list
@blueprint.route("/loans/<int:loan_id>/edit")
def edit_loan(loan_id):
	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute("SELECT * FROM Loans WHERE loan_id = %s", (loan_id,))
			loan = cursor.fetchone()

	if not loan:
		return "Loan not found", 404

	return render_template("loan_edit.html", loan=loan)


# update loans
@blueprint.route("/loans/<int:loan_id>/update", methods=["POST"])
def update_loan(loan_id):

	book_id = request.form["book_id"]
	borrower_id = request.form["borrower_id"]
	loan_date = request.form["loan_date"]
	due_date = request.form["due_date"]
	return_date = request.form.get("return_date", "")
	if return_date == "":
		return_date = None

	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute(
				"""
				UPDATE Loans
				SET book_id = %s,
					borrower_id = %s,
					loan_date = %s,
					due_date = %s,
					return_date = %s
				WHERE loan_id = %s
			""",
				(book_id, borrower_id, loan_date, due_date, return_date, loan_id),
			)

			conn.commit()
	return redirect("/loans")  # Go to the /loans page


# confirm delete page
@blueprint.route("/loans/<int:loan_id>/confirm_delete")
def confirm_delete(loan_id):
	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute("SELECT * FROM Loans WHERE loan_id = %s", (loan_id,))
			loan = cursor.fetchone()

	if not loan:
		return "Loan not found", 404

	return render_template("delete_loan.html", loan=loan)


# delete loans compare with the loan_id
@blueprint.route("/loans/<int:loan_id>/delete", methods=["POST"])
def delete_loans(loan_id):
	with db.connection() as conn:
		with conn.cursor(dictionary=True) as cursor:
			cursor.execute("DELETE FROM Loans WHERE loan_id = %s", (loan_id,))
			conn.commit()
	return redirect("/loans")  # Go to the /loans page
