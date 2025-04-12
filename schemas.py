from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime


# ________________________________________Esquema de Usuarios_____________________________________

# Caracteristicas basicas de un usuario
class Usuariobase(BaseModel):
    nombre: str
    correo: str
    
# Caracteristicas de un usuario que se va a crear que se heredan  de usuario base
class Crearusuario(Usuariobase):
    contraseña: str


# Mostrar actividades 
class Actividadesmostrar(BaseModel):
    id_actividad: int
    nombre_actividad: str
    descripcion: str
    estado: bool
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

# Mostrar a cada usuario
class Usuariomostrar(Usuariobase):
    id : int
    Actividades : List[Actividadesmostrar] = [] # Lista de actividades vacia por defecto
    
    class Config:
        orm_mode = True
        


# _______________________________________Esquema de Actividades____________________________________

# Datos de actividad base
class Actividadesbase(BaseModel):
    nombre_actividad : str
    descripcion : Optional[str]

# Datos para creae una actividad
class Actividadescrear(Actividadesbase):
    estado : bool = False
    Usuarios_id: int

# Informacion relavante del usuario 
class Usuariosimple(BaseModel):
    id : int
    nombre: str
    correo: str
    
    class Config:
        orm_mode = True

# Que actividades le pertenecen al usuario
class ActividadesUsuarios(Actividadesbase):
    id_actividad : int
    estado: bool
    fecha_creacion : datetime
    Usuario : Usuariosimple # Datos del usuario asociado
    
    class Config:
        orm_mode = True