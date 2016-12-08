import sys
#Modulos necesarios para usar Flask
from flask import Flask, render_template, url_for, request, redirect, flash, session
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine, text, and_, or_
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
app.secret_key = 'super_secret_key'

@app.route("/", methods = ['POST', 'GET'])
@app.route("/index", methods = ['POST', 'GET'])
def index():
    """
    Method Index. In charge of displaying the initial page when the user acces the page for the first time (when
    enter the url of the page). Accept two methods: GET and POST.
    When the method is POST:
        -Check if the email and password were introduces.
        -Check if the email has the standard format (somethind@somethingelse.se).
        -Check if the user is already register.
        -Check if the password corresponde to the one of the user.
        -If some or all of the previous is false, it tells the user what is wrong.
        -If all went fine, update the status of the user on the database, by telling it that the user is connected.
        -Extract the username from the email and send the template for the home page of the user.
    If the method is GET:
        -Simple returns the template for the index page.
    """
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
            flash("User not registered or incorrect password")
            return render_template("index.html")
        #Get user from database
        user = session.query(Usuario).filter(Usuario.email == email).one()
        if password != user.contrasena:
            flash("User not registered or incorrect password")
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
    """
    Method for register. Is in charge of displaying the template for the register page. Once the user is succesfully 
    registered, it redirects to the new home page of the user. Accept two methods: GET and POST.
    If the method is POST:
        -Get the necesary data sent by the user to the server (first name, last name, email and passsword).
        -Check if some of the fields are empty.
        -Check if the email has the standard format.
        -Check if the email entered is already on the database.
        -If some of the previous condition is false, it tells the user, and redirect to the register page.
        -If all went fine, extract the username from the email, and create a new instance of Usuario. Fills
        the fields with the corresponding variables sent, and set the status of the user to available on the server.
    If the method is GET:
        -Send the template corresonding to the register page.
    """
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
            flash("User already register")
            return render_template("register.html")

        index = email.find('@')
        username = email[0: index]
        newUser = Usuario(nombre = name, apellido = lastname, email = email, contrasena = pwd, username = username, \
            conectado = True, disponibilidad = True)
        session.add(newUser)
        session.commit()
        return redirect(url_for("home", username = username))
    else:
        return render_template("register.html")

def getImage(uid, profile):
    """
    Get the image asociated with the user. profile: indicate if the image is the profile one.
    Check if the image exists on the database, if not, returns null.
    """
    img = None
    q = session.query(exists().where(and_(Fotos.uid == uid, Fotos.profile == True))).scalar()
    if q:
        picture = session.query(Fotos).filter(and_(Fotos.uid == uid, Fotos.profile == profile)).one()
        img = picture.img_url
    return img

def getContactos(uid):
    """
    Get the contacts of the user with id uid.
    """
    amigos = session.query(Amigos).filter(Amigos.uid == uid).all()
    contactos = []
    ids = []
    for cont in amigos:
        contacto = {}
        ids.append(cont.amigo_id)
        c = session.query(Usuario).filter(Usuario.id == cont.amigo_id).one()
        contacto["name"] = c.nombre + " " + c.apellido
        contacto["img"] = getImage(c.id, True)
        contacto["username"] = c.username
        contactos.append(contacto)
    return (contactos, ids)

def getPublicaciones(uid, u):
    """
    Get the publications corresponding to the user with id: uid.
    u: boolean variable that indicates if the uid correspond to the logged user.
    Check if the user has publications. If not, returns null.
    """
    publicaciones = []
    user = session.query(Usuario).filter(Usuario.id == uid).one()
    q = session.query(exists().where(Publicacion.uid == user.id)).scalar()
    if not q:
        return None
    pub = session.query(Publicacion).filter(Publicacion.uid == uid).order_by(Publicacion.fecha.desc()).all()
    for p in pub:
        publicacion = {}
        publicacion["img"] = getImage(uid, True)
        publicacion["name"] = user.nombre + " " + user.apellido
        publicacion["text"] = p.texto
        publicacion["fecha"] = p.fecha
        publicacion["username"] = user.username
        publicacion["user"] = u
        publicaciones.append(publicacion)
    return publicaciones

#/<string:username>, username
@app.route("/<string:username>/home")
def home(username):
    """
    Method for home. In charge of displaying the home page of the user. It can be accesed via the index, register and
    profile page. It displays the contacts of the user and their publications, includding the ones of the user. Each name 
    of the users is a link to their corresponding home page. It accepts only the GET method.
    The function first check if the user exists, or is already register, on the database. If not, it let know the user and
    redirect it to the index page. This method assumes that the user comes from that page.
    
    It aslo has a condition to check if the user status on the server is connected, to prevent accesing the home page
    from outside, without the proper authorization. In such case, just redirect to the index page without saying nothing.
    
    If all went fine, the method get the contacts of the user (name, image if have, and username) and their ids. With the ids
    of the user, the method get the publications of the friends of the user.
    
    With this, display the corresponding template with the information gathered-
    username: Username of the user.
    """
    q = session.query(exists().where(Usuario.username == username)).scalar()
    if not q:
        flash("User not registered")
        return render_template("index.html")
    user = session.query(Usuario).filter(Usuario.username == username).one()
    if not user.conectado:
        return redirect(url_for("index"))

    #Get the user contacts
    (contactos, ids) = getContactos(user.id)

    #Get the publications of the user and its contacts
    #Get the user publications
    publicaciones = getPublicaciones(user.id, True)
    #Get the user contacts publications
    for aid in ids:
        p = getPublicaciones(aid, False)
        publicaciones.append(p)

    return render_template("home.html", username = username, contacts = contactos, publicaciones = publicaciones)

@app.route("/<string:username>/profile",methods = ['GET', 'POST'])
def profile(username):
    """
    Metod for the profile. In charge of displaying the profile page of the user. It can be accesed only via the home page.
    Displays the image en the full name of the user and its publications. It has a text area where the user can introduce
    text to make a publication. It accepts the methods POST and GET.
    If the method is POST:
        -Check first if the user exists, if not, it redirects to the index page.
        -It is used when the user publish something.
        -Check if something was introduced on the text area, if not, it let know the user and redirect to the profile page.
        -If theres something on the text area, it creates a new instance of the table Publicacion, binding the publication
        to the user, and filling the text field with the recieved information.
        -Redirects to the profile page.
    If the method is GET:
        -Check if the user is connected, if not, it redirects to the index page.
        -Get the user from the database.
        -Get the image of the user from the database.
        -Get the publications of the user.
        -Returns the template of the profile paged filled with the gathered information.
    """
    if request.method == 'POST':
        user = session.query(Usuario).filter(Usuario.username == username).one()
        if not user.conectado:
            return redirect(url_for("index"))
        #Get the text of the publication
        publish = request.form['publish']
        if not publish:
            flash('No text added', "publish")
            return redirect(url_for("profile", username = username))
        #Get the user from database
        user = session.query(Usuario).filter(Usuario.username == username).one()
        #Create a publication entry
        publicacion = Publicacion(uid = user.id, texto = publish)
        session.add(publicacion)
        session.commit()
        return redirect(url_for("profile", username = username))

    else:
        #Get user from database
        user = session.query(Usuario).filter(Usuario.username == username).one()
        if not user.conectado:
            return redirect(url_for("index"))
        name = user.nombre + " " + user.apellido
        #Get image
        img = getImage(user.id, True)
        #Get publication of user
        publicaciones = getPublicaciones(user.id, True)
        return render_template("profile.html", username = username, filename = img, User = name, publicaciones = publicaciones)

@app.route("/<string:username>/friend", methods = ['POST', 'GET'])
def friend(username):
    """
    Method friend. It is use to search for users on the database according to a pattern introduced by the user.
    The pattern can be from a single letter, to a full name. It is accesible from the search button at the top of the 
    home page and profile page of the user, and others users home page. Although the index and register page have also such button, it has no effect.
    It accepts two methods: GET and POST.
    If the method is POST:
        -Check if the user is connected. If not, it redirects to the index page.
        -Check if it was introduce something on the field, it not, returns to the home page (regardless of where it comes
         from), and let the user know there is a field missing.
        -Create a reg exp that the database can recognize, so it can return any match that contains the string passed.
        -Searches in the database to see if at leas one such user exists. If not, it let know user.
        -If at leas one such user exists, it retrieves all the contacts (or contact) that match such pattern, including
        their full name, username, and profile image.
        -Returns the page that contains all the information gathered previously.
    If the method is GET:
        -Check if the user is connected. If not, it redirects to the index page.
        -Redirects to the home page.
    """
    if request.method == 'POST':
        user = session.query(Usuario).filter(Usuario.username == username).one()
        if not user.conectado:
            return redirect(url_for("index"))

        name = request.form['user']
        if not name:
            flash("User not introduced")
            return redirect(url_for("home", username = username))

        likeName = "%" + name + "%"
        #http://stackoverflow.com/questions/3325467/elixir-sqlalchemy-equivalent-to-sql-like-statement
        q = session.query(exists().where( or_(or_(Usuario.username.like(likeName), \
                          Usuario.nombre.like(likeName)), Usuario.apellido.like(likeName)) ) ).scalar()
        if not q:
            flash("User not found")
            return render_template("home.html", username = username)
        friends = session.query(Usuario).filter( or_(or_(Usuario.username.like(likeName), \
                          Usuario.nombre.like(likeName)), Usuario.apellido.like(likeName))).all()
        users = []
        for f in friends:
            user = {}
            if f.username != username:
                user["name"] = f.nombre + " " + f.apellido
                user["username"] = f.username
                user["img"] = getImage(f.id, True)
                users.append(user)
        return render_template("friends_search.html", username = username, usuarios = users)

    else:
        user = session.query(Usuario).filter(Usuario.username == username).one()
        if not user.conectado:
            return redirect(url_for("index"))
        return render_template("home.html", username = username)


@app.route('/<string:username>/logout')
def logout(username):
    """
    Function for loging out the user. Get the user from database and update the status of it.
    Set the user to unavailable.
    """
    #Get user
    user = session.query(Usuario).filter(Usuario.username == username).one()
    #Update status of user
    user.conectado = False
    user.disponibilidad = False
    session.add(user)
    session.commit()
    return redirect(url_for('index'))

@app.route('/<string:username>/friend/<string:friend>')
def contact(username, friend):
    """
    Function Contact. Displays the home page of a friend of the contact. It differs from home page of the user, in that
    the user can access only the wall and the view the photos of the user. Only accepts the GET method.
    In the wall page it displays all the publications of and to the user.
    It displays a text area where the user can publish to the friend (not implemented yet).

    First check if the user is connected to the server, if not, redirect to the index page. It prevents accesing the page
    without the proper authorization. Then check if the friend actually exists on the database, if not, it let know the user
    and returns to the home page of the user.

    If all went fine, it get the name of the user, it image, and the publications of the friend.
    Returns the template of the friend's home page.
    """
    user = session.query(Usuario).filter(Usuario.username == username).one()
    if not user.conectado:
        return redirect(url_for("index"))
    q = session.query(exists().where(Usuario.username == friend)).scalar()
    if not q:
        flash("Friend not existing")
        return redirect(url_for("home", username = username))

    fri = session.query(Usuario).filter(Usuario.username == friend).one()
    name = fri.nombre + " " + fri.apellido
    #Get image
    img = getImage(fri.id, True)
    #Get publication of user
    q = session.query(exists().where(Publicacion.uid == fri.id)).scalar()
    publicaciones = getPublicaciones(fri.id, False)
    return render_template("friend.html", username = username, friendname = friend, filename = img, User = name, publicaciones = publicaciones)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
