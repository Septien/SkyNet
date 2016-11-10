import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

#Hazle saber a SQLAlchemy que nuestras clases corresponden a tablas
Base = declarative_base()

#Tabla usuario
class Usuario(Base):
    #Nombre de la tabla
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True)
    nombre = Column(String, nullable = False)
    apellido = Column(String, nullable = False)
    fechaDeNacimiento = Column(DateTime)
    email = Column(String, nullable = False)
    genero = Column(String(1))
    contrasena = Column(String, nullable = False)
    disponibilidad = (Boolean, default = False)
    conectado = (Boolean, default = False)

#Tabla Publicacion
class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key = True)
    texto = Column(String)
    fecha = Column(DateTime)
    num_likes = Column(Integer, default = 0)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
