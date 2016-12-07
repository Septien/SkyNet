"""
	Suit of tests for server of the SkyNet social network.
"""


import os
import sys
import unittest
import flask

import skynet_server
#Modulos necesario para usar SQLAlchemy y base de datos
from sqlalchemy import create_engine, text, and_, or_
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Usuario, Fotos, Publicacion, Amigos, Etiquetas, Chat, Mensaje

class SkynetTestCase(unittest.TestCase):
	def setUp(self):
		skynet_server.app.config['TESTING'] = True
		self.app = skynet_server.app.test_client()
		self.app.secret_key = 'super_secret_key'
		engine = create_engine("mysql+pymysql://root:12345@localhost/")
		engine.execute("USE skynet")
		Base.metadata.bind = engine
		#Crear sesion para comunicarse con la base de datos
		self.DBSession = sessionmaker(bind = engine)
		

	def tearDown(self):
		pass

	def login(self, email, password, route):
		"""For testing the log in"""
		return self.app.post(route, data = dict(email = email, password = password), follow_redirects = True)

	def test_index(self):
		"""
		Test the method index. If the method of the request is GET, just verify that the returned HTML
		is correctly formatted. Check if the strings 'Username', 'Password' and 'Login' are present in the file.
		If the methos is POST, there are many things to verify:
			-If there is no password or email on the request form, indicate that a field is missing.
			-If the format of the email is incorrect, indicate to the user that email format is wrong
			-If the user is not in the database or the password is incorrect: indicate it to the user.
			-If all went fine, check that the status of the user is correctly updated on the data base and the 
			returned template is the adecuate.
		"""
		session = self.DBSession()
		#Tests for GET method
		rv = self.app.get("/")
		assert "Username" in rv.data
		assert "Password" in rv.data
		assert "Login" in rv.data
		rv = self.app.get("/index")
		assert "Username" in rv.data
		assert "Password" in rv.data
		assert "Login" in rv.data

		#Tests for POST method
		#Testing log in
		rv = self.login("johns@correo.com", "", "/")
		assert "Missing field" in rv.data
		rv = self.login("", "12345", "/")
		assert "Missing field" in rv.data
		rv = self.login("johns", "12345", "/")
		assert "Incorrect email format" in rv.data
		rv = self.login("john@correo.com", "12345", "/")
		assert "User not registered or incorrect password" in rv.data
		rv = self.login("johns@correo.com", "1234", "/")
		assert "User not registered or incorrect password" in rv.data

		rv = self.login("johns@correo.com", "12345", "/")
		#Get the user from the database
		user = session.query(Usuario).filter(Usuario.email == "johns@correo.com").one()
		assert user.conectado == True
		assert user.disponibilidad == True
		#Test correct redirect
		assert "johns" in rv.data

	def register(self, name, lastname, email, password):
		return self.app.post("/register", data = dict(name = name, LastName = lastname, email = email, \
			password = password), follow_redirects = True)

	def test_register(self):
		"""
		Test the method register. If the method of the request is GET, just verify that the returned HTML
		is correctly formatted. Check if the strings 'First Name', 'Last Name', 'Your Email', 'Password'
		and 'Register' are present in the file.
		If the methos is POST, there are many things to verify:
			-If there is no first name, last name, email or password on the request form, indicate that a field is missing.
			-If the format of the email is incorrect, indicate to the user that email format is wrong
			-If the user is already in the database: indicate it to the user.
			-If all went fine, check that the user is correctly added to the database and the
			status of the user is correctly updated on the data base and the returned template is the adecuate.
		"""
		session = self.DBSession()
		#Test the GET method
		rv = self.app.get("/register")
		assert "First Name" in rv.data
		assert "Last Name" in rv.data
		assert "Your Email" in rv.data
		assert "Password" in rv.data
		assert "Register" in rv.data

		#Test the POST method
		#Check for missing fields
		rv = self.register("", "", "", "")
		assert "Missing field" in rv.data
		rv = self.register("Angry", "Bird", "blue_bird@angry.ab", "")
		assert "Missing field" in rv.data
		rv = self.register("Angry", "Bird", "", "angryme")
		assert "Missing field" in rv.data
		rv = self.register("Angry", "", "blue_bird@angry.ab", "angryme")
		assert "Missing field" in rv.data
		rv = self.register("", "Bird", "blue_bird@angry.ab", "angryme")
		assert "Missing field" in rv.data

		#Incorrect email format
		rv = self.register("Angry", "Bird", "blue_bird@angry", "angryme")
		assert "Incorrect email format" in rv.data

		#Already registered user
		rv = self.register("John", "Snow", "johns@correo.com", "12345")
		assert "User already register" in rv.data

		#Check correct add of user to database and update status
		rv = self.register("Angry", "Bird", "blue_bird@angry.ab", "angryme")
		q = session.query(exists().where(Usuario.username == "blue_bird")).scalar()
		assert q == True
		user = session.query(Usuario).filter(Usuario.email == "blue_bird@angry.ab").one()
		assert user.nombre == "Angry"
		assert user.apellido == "Bird"
		assert user.email == "blue_bird@angry.ab"
		assert user.contrasena == "angryme"
		assert user.username == "blue_bird"
		assert user.conectado == True
		assert user.disponibilidad == True


if __name__ == '__main__':
	unittest.main()
