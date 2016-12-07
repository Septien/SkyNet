"""
	Suit of tests for server of the SkyNet social network.
"""


import os
import sys
import unittest

import skynet_server
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine, text, and_, or_
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Usuario, Fotos, Publicacion, Amigos, Etiquetas, Chat, Mensaje

engine = create_engine("mysql+pymysql://root:12345@localhost/")
engine.execute("USE skynet")
Base.metadata.bind = engine

#Crear sesion para comunicarse con la base de datos
DBSession = sessionmaker(bind = engine)

class SkynetTestCase(unittest.TestCase):
	def setUp(self):
		skynet_server.app.config['TESTING'] = True
		self.app = skynet_server.app.test_client()
		self.app.secret_key = 'super_secret_key'
		self.session = DBSession()

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()