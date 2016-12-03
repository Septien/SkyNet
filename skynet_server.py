import sys
#Modulos necesarios para usar Flask
from flask import Flask, render_template, url_for, request, redirect, flash, session
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine, text
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Usuario, Fotos, Publicacion, Amigos, Etiquetas, Chat, Mensaje
#For regular expresions
import re

#Crear motor de base de datos
engine = create_engine("mysql+pymysql://root:12345@localhost/")
engine.execute("USE skynet")
Base.metadata.bind = engine

#Create reg exp for verifying email
emailPattern = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
regexp = re.compile(emailPattern)

#Crear sesion para comunicarse con la base de datos
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Inicializa la app de Flask
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
@app.route("/index", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            flash("Missing field")
            return render_template("index.html")

        #Check for validity of email
        r = regexp.match(email)
        if r == None:
            flash("Incorrect email format")
            return render_template("index.html")

        #http://stackoverflow.com/questions/1676551/best-way-to-test-if-a-row-exists-in-a-mysql-table
        #http://stackoverflow.com/questions/7646173/sqlalchemy-exists-for-query
        q = session.query(exists().where(Usuario.email == email)).scalar()
        if not q:
            flash("User no registered or incorrect password")
            return render_template("index.html")
        user = session.query(Usuario).filter(email == email).one()
        if password != user.contrasena:
            flash("User no registered or incorrect password")
            return render_template("index.html")
        index = email.find('@')
        username = email[0: index]
        user.conectado = True
        user.disponibilidad = True
        session.add(user)
        session.commit()
        return redirect(url_for("home", username = username))
    else:
        return render_template("index.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['LastName']
        email = request.form['email']
        pwd = request.form['password']

        if not name or not lastname or not email or not pwd:
            flash("Missing field")
            return render_template("register.html")

        #Check for validity of email
        r = regexp.match(email)
        if r == None:
            flash("Incorrect email format")
            return render_template("register.html")

        index = email.find('@')
        username = email[0: index]
        newUser = Usuario(nombre = name, apellido = lastname, email = email, contrasena = pwd, username = username)
        session.add(newUser)
        session.commit()
        return render_template("register.html")
    else:
        return render_template("register.html")

#/<string:username>, username
@app.route("/<string:username>/home")
def home(username):
    q = session.query(exists().where(Usuario.username == username)).scalar()
    if not q:
        flash("User no registered")
        return render_template("index.html")
    q = session.query(Usuario).filter(Usuario.username == username)

    return render_template("home.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
