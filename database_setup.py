import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date, text
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
    #Primary key
    id = Column(Integer, primary_key = True)

    #User data
    nombre = Column(String(40), nullable = False)
    apellido = Column(String(40), nullable = False)
    fechaDeNacimiento = Column(DateTime)
    username = Column(String(40))
    email = Column(String(40), nullable = False)
    genero = Column(String(1))
    contrasena = Column(String(16), nullable = False)
    disponibilidad = Column(Boolean, default = False)   #On chat
    conectado = Column(Boolean, default = False)        #To server

#Tabla de fotos
class Fotos(Base):
    __tablename__ = 'fotos'
    #Primary key
    id = Column(Integer, primary_key = True)

    #Foregin key
    uid = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship(Usuario)

    #The image
    img = Column(BLOB)

#Tabla Publicacion
class Publicacion(Base):
    __tablename__ = 'publicacion'
    #Primary key
    id = Column(Integer, primary_key = True)

    #Foreign key
    uid = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship(Usuario)
    fid = Column(Integer, ForeignKey('fotos.id'))
    fotos = relationship(Fotos)

    #Needed fields
    texto = Column(TEXT)
    #http://stackoverflow.com/questions/6992321/how-to-set-default-on-update-current-timestamp-in-mysql-with-sqlalchemy
    fecha = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    num_likes = Column(Integer, default = 0)

#Tabla de etiquetas
class Etiquetas(Base):
    __tablename__ = 'etiquetas'
    #Primary and foreign keys
    pid = Column(Integer, ForeignKey('publicacion.id'), primary_key = True)
    publicacion = relationship(Publicacion)
    uid = Column(Integer, ForeignKey('usuario.id'), primary_key = True)
    usuario = relationship(Usuario)

#Tabla de amigos
class Amigos(Base):
    __tablename__ = 'amigos'
    #Foregin and primary keys
    uid = Column(Integer, ForeignKey('usuario.id'), primary_key = True)
    amigo_id = Column(Integer, ForeignKey('usuario.id'), primary_key = True)
    usuario = relationship(Usuario, foreign_keys = [uid])
    amigo = relationship(Usuario, foreign_keys = [amigo_id])

    #Information needed
    permiso_compartir = Column(Boolean, default = True)
    ver_contenido = Column(Boolean, default = True)
    bloqueado = Column(Boolean, default = False)
    notificaciones = Column(Boolean, default = True)

#Tabla de chat
class Chat(Base):
    __tablename__ = 'chat'
    #Primary keys
    id = Column(Integer, primary_key = True)

    #Foreign keys
    uid = Column(Integer, ForeignKey('usuario.id'))
    amigo_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship(Usuario, foreign_keys = [uid])
    amigo = relationship(Usuario, foreign_keys = [amigo_id])

#Tabla de mensajes de chat
class Mensaje(Base):
    __tablename__ = 'mensaje'
    #Primary key
    id = Column(Integer, primary_key = True)

    #Foreign key to chat
    cid = Column(Integer, ForeignKey('chat.id'))
    chat = relationship(Chat)

    #Foreign key to user
    uid = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship(Usuario)

    #Foreign key to images
    iid = Column(Integer, ForeignKey('fotos.id'))
    fotos = relationship(Fotos)

    #Needed information
    texto = Column(TEXT)
    fecha = Column(TIMESTAMP, server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    ultimo = Column(Boolean, default = True)

#http://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
engine = create_engine("mysql+pymysql://root:12345@localhost/")
#http://stackoverflow.com/questions/10770377/howto-create-db-mysql-with-sqlalchemy
engine.execute("DROP DATABASE IF EXISTS skynet")
engine.execute("CREATE DATABASE skynet")
engine.execute("USE skynet")
Base.metadata.create_all(engine)
