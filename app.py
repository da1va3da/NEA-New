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

        conn2 = sqlite3.connect('accounts.db')
        cursor = conn2.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user2 = cursor.fetchone()
        conn.close()

        if user:
            connection = sqlite3.connect("accounts.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            account = cursor.fetchone()
            

            if account:
                session['user'] = email
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            elif user2: 
                flash('Incorrect password. Try again.')
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
    connection = sqlite3.connect("schooldata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Teachers WHERE Email=?", (session['user'],))
    teacher = cursor.fetchall()
    if 'user' in session:
        for t in teacher:
            firstname = t[1]
            surname = t[2]
            gender = t[3]
            email = t[4]
            
        return render_template("dashboard.html", user=session['user'], firstname=firstname, surname=surname, gender=gender, email=email)
    else:
        flash('You must be logged in to view the dashboard.')
        return redirect(url_for('login'))

@app.route('/messages') # Messages route
def messages():
    if 'user' in session:
        return render_template("messages.html")
    else:
        flash('You must be logged in to view messages.')


@app.route('/students') # Students route
def students():
    connection = sqlite3.connect("schooldata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Teachers WHERE Email=?", (session['user'],))
    teacher = cursor.fetchall()
    if 'user' in session:
        for t in teacher:
            role = t[5]
        if role == "A":
            cursor.execute("SELECT * FROM Students")
            students = cursor.fetchall()
            return render_template("admin_students.html", students=students) 
        else:
            cursor.execute("SELECT * FROM Students")
            students = cursor.fetchall()
            return render_template("students.html", students=students)
    else:
        flash('You must be logged in to view students.')
        return redirect(url_for('login'))
    

@app.route('/add_student', methods=['GET', 'POST']) # Add Student route
def add_student():
    if 'user' in session:
        if request.method == 'POST':
            firstname = request.form.get('firstname')
            surname = request.form.get('surname')
            gender = request.form.get('gender')
            dob = request.form.get('dob')       
            yeargroup = request.form.get('yeargroup')
            mastery = request.form.get('mastery')
            email = request.form.get('email')

            parentname = request.form.get('parentname')
            parentnumber = request.form.get('parentnumber')
            address = request.form.get('address')
            nationality = request.form.get('nationality')
            countryofbirth = request.form.get('countryofbirth')
            enrollmentdate = request.form.get('enrollmentdate')

            conditions = request.form.get('conditions')
            medication = request.form.get('medication')
            allergies = request.form.get('allergies')
            needs = request.form.get('needs')


            connection = sqlite3.connect("schooldata.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Students (Firstname, Surname, Gender, DOB) VALUES (?, ?, ?, ?)", (firstname, surname, gender, dob))
            connection.commit()
            connection.close()
            flash('Student added successfully!')
            return redirect(url_for('students'))
        return render_template("add_student.html")
    
if __name__ == "__main__": # Run the app
    app.run(debug=True)





