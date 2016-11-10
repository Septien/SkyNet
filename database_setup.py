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
    disponibilidad = Column(Boolean, default = False)
    conectado = Column(Boolean, default = False)

#Tabla de fotos
class Fotos(Base):
    __tablename__ = 'fotos'
    id = Column(Integer, primary_key = True)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    location = Column(String)

#Tabla Publicacion
class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key = True)
    texto = Column(String)
    fecha = Column(DateTime)
    num_likes = Column(Integer, default = 0)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    foto = relationship(Fotos)
    fid = Column(Integer, ForeignKey('foto.id'))

#Tabla de etiquetas
class Etiquetas(Base):
    __tablename__ = 'etiquetas'
    publicacion = relationship(Publicacion)
    pid = Column(Integer, ForeignKey('publicacion.id'), primary_key = True)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'), primary_key = True)

#Tabla de amigos
class Amigos(Base):
    __tablename__ = 'amigos'
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'), primary_key = True)
    amigo_id = Column(Integer, ForeignKey('usuario.id'), primary_key = True)
    permiso_compartir = Column(Boolean, default = True)
    ver_contenido = Column(Boolean, default = True)
    Boolean = Column(Boolean, default = False)
    notificaciones = Column(Boolean, default = True)

#Tabla de chat
class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key = True)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    amigo_id = Column(Integer, ForeignKey('usuario.id'))

#Tabla de mensajes de chat
class Mensaje(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key = True)
    chat = relationship(Chat)
    cid = Column(Integer, ForeignKey('chat.id'))
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    texto = Column(String)
    fecha = Column(DateTime)
    img = relationship(Fotos)
    iid = Column(Integer, ForeignKey('img.id'))
    ultimo = Column(Boolean, default = True)

engine = create_engine("mysql + pmysql://root:12345@localhost/test?charset=utf8")
Base.metadata.create_all(engine)
