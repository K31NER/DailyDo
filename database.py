# Configuracion de la base de datos
# Importamos la librerias
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definimos la direccion de la base de datos
SQL_DATABASE= "sqlite:///./ToDo.db"

# Creamos la base de datos y el motor(No es necesario el connect_args en todos los casos, solo se pone si quieres concurrencia)
engine = create_engine(SQL_DATABASE,connect_args={"check_same_thread": False})

# Crea el manejador de sesionies asociandoe el engine y definiendo el autocommit y autoflush en false
sessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

# Creamos una base para usarla en las clases para crear las tablas
Base = declarative_base()