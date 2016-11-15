#Modulos necesarios para usar Flask
from flask import Flask, render_template, url_for, request, redirect, flash
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Usuario, Fotos, Publicación, Etiquetas, Amigos, Chat, Mensaje

#Crear motor de base de datos
engine = create_engine("mysql+pymysql://root:12345@localhost/")
engine.execute("USE skynet")
Base.metadata.bind = engine

#Crear sesion para comunicarse con la base de datos
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Inicializa la app de Flask
app = Flask(__name__)
