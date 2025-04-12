# Creacion de los modelos

# Importamos las librerias 

from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey # Parametros a usar en la tabla
from sqlalchemy.sql import func # Para la fecha de creacion
from sqlalchemy.orm import relationship # Para las relaciones entre tablas
from database import Base # Llamamos a la base de las tablas



# hacemos la clase con herrencia de Basemodel

class Usuarios(Base):
    __tablename__ = "Usuarios"
    
    id = Column(Integer, primary_key = True , index= True)
    nombre = Column(String(50),nullable= False)
    correo = Column(String(50), nullable= False)
    contraseña = Column(String(500), nullable= False)
    
    # Relacion uno a muchos
    Actividades = relationship("Actividades", back_populates="Usuarios")


class Actividades(Base):
    __tablename__ = "Actividades"
    
    id_actividad = Column(Integer, primary_key = True , index= True)
    nombre_actividad = Column(String(50),nullable= False)
    descripcion = Column(String(100),nullable= False)
    estado = Column(Boolean,default= False)
    fecha_creacion = Column(DateTime, nullable= False, server_default = func.now())
    
    # LLave foranea que hace referencia a la tabla de usuarios 
    Usuarios_id = Column(Integer,ForeignKey("Usuarios.id"))
    
    # Relacion 
    Usuarios = relationship("Usuarios", back_populates="Actividades")
    
    
