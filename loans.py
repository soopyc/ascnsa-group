from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector



blueprint = Blueprint("loans", __name__)
DB_CONFIG = { # configure the database
	"host": "127.0.0.1", 
	"user": "user",
	"password": "userresu",
	"database": "library_app",
	"port": 3306,
}
# show loans details
@blueprint.route("/loans")
def show_loans():
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Loans") #get all from Loans table
	rows = cursor.fetchall()
	cursor.close()
	conn.close()
return render_template('loans.html', loans=rows)



# craete new loans
@blueprint.route("/loans/create", methods=['GET', 'POST'])
def create_loans():
	 if request.method == 'GET':
		return render_template('create_loan.html')
	 conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("INSERT INTO Loans ( book_id, borrower_id,loan_date,due_date,return_date) VALUES ( %s,%s,CURDATE(),CURDATE() + 14, NULL);")
	cursor.close()
	conn.close()
return redirect('/loans')



# show the edit loans list
@blueprint.route("/loans/<int:loan_id>/edit")
def edit_loan(loan_id):
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Loans WHERE loan_id = %s", (loan_id,))
	loan = cursor.fetchone()
	cursor.close()
	conn.close()
	
	if not loan:
		return "Loan not found", 404
	
	return render_template("loan_edit.html", loan=loan)
what is this work for , give to the output to see


# update loans
@blueprint.route("/loans/<int:loan_id>/update", methods=["POST"])
def update_loan(loan_id):
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor()
	
	book_id = request.form["book_id"]
	borrower_id = request.form["borrower_id"]
	loan_date = request.form["loan_date"]
	due_date = request.form["due_date"]
	return_date = request.form.get("return_date", None)
	
	cursor.execute("""
		UPDATE Loans 
		SET book_id = %s, 
			borrower_id = %s, 
			loan_date = %s, 
			due_date = %s, 
			return_date = %s
		WHERE loan_id = %s
	""", (book_id, borrower_id, loan_date, due_date, return_date, loan_id))
	
	conn.commit()
	cursor.close()
	conn.close()
	return redirect("/loans")#Go to the /loans page

#confirm delete page
@blueprint.route("/loans/<int:loan_id>/confirm_delete")
def confirm_delete(loan_id):
	conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Loans WHERE loan_id = %s", (loan_id,))
	loan = cursor.fetchone()
	cursor.close()
	conn.close()
	
	if not loan:
		return "Loan not found", 404
	
	return render_template("delete_loan.html", loan=loan)

# delete loans compare with the loan_id 
@blueprint.route("/loans/<int:loan_id>/delete", methods=['POST'])
def delete_loans(loan_id):
	 conn = mysql.connector.connect(**DB_CONFIG)
	cursor = conn.cursor(dictionary=True)
	cursor.execute("DELETE FROM Loans WHERE loan_id = %s", (loan_id,))
	conn.commit()
	cursor.close()
	conn.close()
return redirect('/loans')   #Go to the /loans page



