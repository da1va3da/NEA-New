#IMPORTS
from flask import Flask, render_template, session, abort, redirect, url_for, request


app = Flask(__name__)

@app.route('/') # Home route
def home():
    return render_template("home.html")


@app.route('/login') # Login route
def login():
    return render_template("login.html")








