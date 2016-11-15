import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date
#http://docs.sqlalchemy.org/en/latest/dialects/mysql.html?highlight=text%20mysql#sqlalchemy.dialects.mysql.LONGTEXT
from sqlalchemy.dialects.mysql import TEXT, BLOB, TIMESTAMP
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
    nombre = Column(String(40), nullable = False)
    apellido = Column(String(40), nullable = False)
    fechaDeNacimiento = Column(DateTime)
    email = Column(String(40), nullable = False)
    genero = Column(String(1))
    contrasena = Column(String(16), nullable = False)
    disponibilidad = Column(Boolean, default = False)
    conectado = Column(Boolean, default = False)

#Tabla de fotos
class Fotos(Base):
    __tablename__ = 'fotos'
    id = Column(Integer, primary_key = True)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    img = Column(BLOB)

#Tabla Publicacion
class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key = True)
    texto = Column(TEXT)
    fecha = Column(TIMESTAMP)
    num_likes = Column(Integer, default = 0)
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    fotos = relationship(Fotos)
    fid = Column(Integer, ForeignKey('fotos.id'))

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
    bloqueado = Column(Boolean, default = False)
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
    __tablename__ = 'mensaje'
    id = Column(Integer, primary_key = True)
    chat = relationship(Chat)
    cid = Column(Integer, ForeignKey('chat.id'))
    usuario = relationship(Usuario)
    uid = Column(Integer, ForeignKey('usuario.id'))
    texto = Column(TEXT)
    fecha = Column(TIMESTAMP)
    fotos = relationship(Fotos)
    iid = Column(Integer, ForeignKey('fotos.id'))
    ultimo = Column(Boolean, default = True)

#http://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
engine = create_engine("mysql+pymysql://root:12345@localhost/")
#http://stackoverflow.com/questions/10770377/howto-create-db-mysql-with-sqlalchemy
engine.execute("DROP DATABASE IF EXISTS skynet")
engine.execute("CREATE DATABASE skynet")
engine.execute("USE skynet")
Base.metadata.create_all(engine)
