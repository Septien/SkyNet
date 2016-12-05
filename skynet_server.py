import sys
#Modulos necesarios para usar Flask
from flask import Flask, render_template, url_for, request, redirect, flash, session
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine, text, and_
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
        #Check if user exists
        q = session.query(exists().where(Usuario.email == email)).scalar()
        if not q:
            flash("User no registered or incorrect password")
            return render_template("index.html")
        #Get user from database
        user = session.query(Usuario).filter(Usuario.email == email).one()
        if password != user.contrasena:
            flash("User no registered or incorrect password")
            return render_template("index.html")
        index = email.find('@')
        username = email[0: index]
        #Update status of user
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

        #Check if user not already exists
        q = session.query(exists().where(Usuario.email == email)).scalar()
        if q:
            flash("User already redister")
            return render_template("register.html")

        index = email.find('@')
        username = email[0: index]
        newUser = Usuario(nombre = name, apellido = lastname, email = email, contrasena = pwd, username = username)
        session.add(newUser)
        session.commit()
        return redirect(url_for("home", username = username))
    else:
        return render_template("register.html")

#/<string:username>, username
@app.route("/<string:username>/home")
def home(username):
    q = session.query(exists().where(Usuario.username == username)).scalar()
    if not q:
        flash("User no registered")
        return render_template("index.html")
    user = session.query(Usuario).filter(Usuario.username == username).one()
    #Get image
    img = None
    q = session.query(exists().where(and_(Fotos.uid == user.id, Fotos.profile == True))).scalar()
    if q:
        picture = session.query(Fotos).filter(and_(Fotos.uid == user.id, Fotos.profile == True)).one()
        img = picture.img_url
    amigos = session.query(Amigos).filter(Amigos.uid == user.id).all()
    #Get the user contacts
    contactos = []
    ids = []
    for cont in amigos:
        contacto = {}
        ids.append(cont.amigo_id)
        c = session.query(Usuario).filter(Usuario.id == cont.amigo_id).one()
        contacto["name"] = c.nombre + " " + c.apellido
        q = session.query(Fotos).filter(and_(Fotos.uid == c.id, Fotos.profile == True)).one()
        contacto["img"] = q.img_url
        contactos.append(contacto)

    #Get the publications of the user and its contacts
    publicaciones = []
    #Get the user publications
    pub = session.query(Publicacion).filter(Publicacion.uid == user.id).all()
    for p in pub:
        publicacion = {}
        publicacion["img"] = img
        publicacion["name"] = user.nombre + " " + user.apellido
        publicacion["text"] = p.texto
        publicacion["fecha"] = p.fecha
        publicaciones.append(publicacion)
    #Get the user contacts publications
    for aid in ids:
        c = session.query(Usuario).filter(Usuario.id == aid).one()
        pub = session.query(Publicacion).filter(Publicacion.uid == aid).all()
        for p in pub:
            publicacion = {}
            if q:
                picture = session.query(Fotos).filter(and_(Fotos.uid == aid, Fotos.profile == True)).one()
                publicacion["img"] = picture.img_url
            publicacion["name"] = c.nombre + " " + c.apellido
            publicacion["text"] = p.texto
            publicacion["fecha"] = p.fecha
            publicaciones.append(publicacion)

    return render_template("home.html", username = username, contacts = contactos, publicaciones = publicaciones)

@app.route("/<string:username>/profile",methods = ['GET', 'POST'])
def profile(username):
    if request.method == 'POST':
        #Get the text of the publication
        publish = request.form['publish']
        #Get the user from database
        user = session.query(Usuario).filter(Usuario.username == username).one()
        #Create a publication entry
        publicacion = Publicacion(uid = user.id, texto = publish)
        session.add(publicacion)
        session.commit()
        return redirect(url_for("profile.html", username = username))

    else:
        #Get user from database
        user = session.query(Usuario).filter(Usuario.username == username).one()
        name = user.nombre + " " + user.apellido
        #Get image
        img = None
        q = session.query(exists().where(and_(Fotos.uid == user.id, Fotos.profile == True))).scalar()
        if q:
            picture = session.query(Fotos).filter(and_(Fotos.uid == user.id, Fotos.profile == True)).one()
            img = picture.img_url
        #Get publication of user
        q = session.query(exists().where(Publicacion.uid == user.id)).scalar()
        publicaciones = []
        if q:
            pub = session.query(Publicacion).filter(Publicacion.uid == user.id).all()
            for p in pub:
                publicacion = {}
                publicacion["img"] = img
                publicacion["name"] = name
                publicacion["text"] = p.texto
                publicacion["fecha"] = p.fecha
                publicaciones.append(publicacion)
        return render_template("profile.html", username = username, filename = img, User = name, publicaciones = publicaciones)

@app.route("/<string:username>/friend", methods = ['POST', 'GET'])
def friend(username):
    if request.method == 'POST':
        name = request.form['user']
        if not name:
            flash("User not introduced")
            return redirect(url_for("home", username = username))

        likeName = "%" + name + "%"
        #http://stackoverflow.com/questions/3325467/elixir-sqlalchemy-equivalent-to-sql-like-statement
        q = session.query(exists().where(Usuario.username.like(likeName))).scalar()
        if not q:
            flash("User not found")
            return render_template("home.html", username = username)
    else:
        return render_template("home.html", username = username)

    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
