import sys
#Modulos necesarios para usar Flask
from flask import Flask, render_template, url_for, request, redirect, flash
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database_setup as db

#Crear motor de base de datos
engine = create_engine("mysql+pymysql://root:12345@localhost/")
engine.execute("USE skynet")
db.Base.metadata.bind = engine

#Crear sesion para comunicarse con la base de datos
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Inicializa la app de Flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
