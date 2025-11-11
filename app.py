#IMPORTS
from flask import Flask, render_template, session, abort, redirect, url_for, request, flash
import sqlite3
from flask_mail import Mail, Message
import random 


app = Flask(__name__)
app.secret_key = 'StudsightSecretKey123'

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'doludavid@gmail.com'
app.config['MAIL_PASSWORD'] = 'David12345!'
app.config['MAIL_DEFAULT_SENDER'] = 'doludavid15@gmail.com'

mail = Mail(app)

def generate_pin():
    return str(random.randint(100000, 999999))


@app.route('/') # Home route
def home():
    return render_template("home.html")


connection = sqlite3.connect("accounts.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT, password TEXT)''')
connection.commit()
connection.close()



@app.route('/register', methods=['GET', 'POST']) # Register route
def register():
    if request.method == 'POST':
        email = request.form.get('email')


        conn = sqlite3.connect('schooldata.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Teachers WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            conn2 = sqlite3.connect('accounts.db')
            cursor = conn2.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user2 = cursor.fetchone()
            conn2.close()

            if user2:
                flash('Account already exists. Please login.')
                return redirect(url_for('login'))
            else:
                password = request.form.get('password')
                confiirm_password = request.form.get('confirm_password')
                if password != confiirm_password:
                    flash('Passwords do not match. Please try again.')
                    return redirect(url_for('register'))
                
                conn2 = sqlite3.connect('accounts.db')
                cursor = conn2.cursor()
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn2.commit()
                conn2.close()
                flash('Registration successful! Please login.')
                return redirect(url_for('login'))
        else:
            flash('Email not found in teacher records. Please contact admin.')
            return redirect(url_for('register'))
    return render_template("register.html")





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
                flash('No account found with that email. Please register.')
                return redirect(url_for('register'))
        
        else:
            flash('Invalid email. Try again.')

    return render_template("login.html")




@app.route('/forgot_password') # Forgot Password route
def forgot_password():
    connection = sqlite3.connect("accounts.db")
    cursor = connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            pin = generate_pin()
            msg = Message('Password Reset PIN', recipients=[email])
            msg.body = f'Your password reset PIN is: {pin}'
            mail.send(msg)

            flash('Password reset link sent to your email.')
        else:
            flash('Email not found. Please try again.')
    return render_template("forgot_password.html")





@app.route('/reset_password') # Reset Password route
def reset_password():
    connection = sqlite3.connect("accounts.db")
    cursor = connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            connection.commit()
            flash('Password reset successful!')

            return redirect(url_for('login'))
        else:
            flash('Email not found. Please try again.')
    return render_template("reset_password.html")





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





