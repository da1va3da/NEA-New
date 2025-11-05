#IMPORTS
from flask import Flask, render_template, session, abort, redirect, url_for, request, flash
import sqlite3


app = Flask(__name__)
app.secret_key = 'StudsightSecretKey123'

@app.route('/') # Home route
def home():
    return render_template("home.html")


connection = sqlite3.connect("accounts.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT, password TEXT)''')
connection.commit()
connection.close()


@app.route('/login', methods=['GET', 'POST']) # Login route
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect('schooldata.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Teachers WHERE Email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            connection = sqlite3.connect("accounts.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            account = cursor.fetchone()
            

            if account:
                session['user'] = email
                flash('Login successful!')
                return redirect(url_for('dashboard'))#
            else:
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                connection.commit()
                connection.close()
                session['user'] = email
                flash('Account created and logged in!')
                return redirect(url_for('dashboard'))
        
        else:
            flash('Invalid email. Try again.')

    return render_template("login.html")




@app.route('/dashboard') # Dashboard route
def dashboard():
    if 'user' in session:
        return render_template("dashboard.html", user=session['user'])
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))


if __name__ == "__main__": # Run the app
    app.run(debug=True)






