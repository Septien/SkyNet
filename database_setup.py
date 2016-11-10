import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#Hazle saber a SQLAlchemy que nuestras clases corresponden a tablas
Base = declarative_base()
