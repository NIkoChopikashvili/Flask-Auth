from enum import unique
import re
from flask import Flask, redirect, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
from sqlalchemy import exc
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False, unique=True)
    passwrd = db.Column(db.String(200))
    email_email = db.Column(db.String(200), unique=True)

@app.route('/logged', methods=["POST", "GET"])
def logged():
    if request.method == "POST":
        crypto_name = request.form['some']
        html = requests.get(f"https://coinmarketcap.com/currencies/{crypto_name}/")
        bs = BeautifulSoup(html.text, "lxml")
        crypto_price = bs.find("div", class_= "priceValue___11gHJ")
        print(crypto_price.text)
    try:
        return render_template("logged.html", crypto_price = crypto_price.text) 
    except UnboundLocalError:
        return render_template('logged.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        username = request.form['user_name']
        password = request.form['user_password']
        email = request.form['email']

        new_user = Data(user_name=username, passwrd=generate_password_hash(password, method='sha256'), email_email=email)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

        return redirect(url_for('home'))

    return render_template("sign_up.html")



@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['user_password']

        user = Data.query.filter_by(email_email=email).first()
        if user:
            if check_password_hash(user.passwrd, password):
                return redirect(url_for('logged'))

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)