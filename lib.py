from flask import Flask, render_template, request, redirect, url_for,flash,session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'library123!@#secure'

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ROOT",  
    database="library_db"
)
cursor = db.cursor(dictionary=True)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()  

        if user:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('home'))
        elif username == 'reader' and password == 'reader123':
            session['username'] = username
            session['role'] = 'public'
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')




# Home page – List all books
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for("login"))
    
    category_query = request.args.get('category')
    #cat specified
    if category_query:
        cursor.execute("SELECT * FROM books WHERE category LIKE %s", ('%' + category_query + '%',))
    #cat not specified
    else:
        cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('home.html', books=books)

# Add new book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        name = request.form['name']
        category = request.form['category']
        cursor.execute("INSERT INTO books (author_name, book_name, category) VALUES (%s, %s, %s)",
                       (author, name, category))
        db.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

# Update book
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        author = request.form['author']
        name = request.form['name']
        category = request.form['category']
        cursor.execute("UPDATE books SET author_name=%s, book_name=%s, category=%s WHERE id=%s",
                       (author, name, category, id))
        db.commit()
        return redirect(url_for('home'))
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    return render_template('update.html', book=book)

# Delete book
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM borrowed_books WHERE book_id = %s", (id,))
    cursor.execute("DELETE FROM returned_books WHERE book_id = %s", (id,))
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    db.commit()
    flash("Book and its related records deleted successfully!", "success")
    return redirect(url_for('home'))


# Borrow book
@app.route('/borrow/<int:id>', methods=['GET', 'POST'])
def borrow(id):
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("INSERT INTO borrowed_books (book_id, borrower_name) VALUES (%s, %s)", (id, name))
        cursor.execute("UPDATE books SET status='Not Available' WHERE id=%s", (id,))
        db.commit()
        return redirect(url_for('home'))
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    return render_template('borrow.html', book=book)

# Return book
@app.route('/return/<int:id>', methods=['GET', 'POST'])
def return_book(id):
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("INSERT INTO returned_books (book_id, returner_name) VALUES (%s, %s)", (id, name))
        cursor.execute("UPDATE books SET status='Available' WHERE id=%s", (id,))
        db.commit()
        return redirect(url_for('home'))
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    return render_template('return.html', book=book)

# View borrow and return history
@app.route('/history')
def history():
    cursor.execute("""
        SELECT bb.id, b.book_name, bb.borrower_name, bb.borrow_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        ORDER BY bb.borrow_date DESC
    """)
    borrowed = cursor.fetchall()

    cursor.execute("""
        SELECT rb.id, b.book_name, rb.returner_name, rb.return_date
        FROM returned_books rb
        JOIN books b ON rb.book_id = b.id
        ORDER BY rb.return_date DESC
    """)
    returned = cursor.fetchall()

    return render_template('history.html', borrowed=borrowed, returned=returned)

#logout

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)                                                                                                              