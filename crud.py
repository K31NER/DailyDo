from sqlalchemy.orm import Session
from models import Actividades,Usuarios
from schemas import Crearusuario, Actividadescrear,ActividadesUsuarios
from typing import List


# ________________________________________Esquema de Usuarios_____________________________________

# Funcion para crear usuario
def crear_usuario(db:Session,usuario: Crearusuario): # Definimos la conexion y el esquema
    # Definimos los datos que recibira en base al model Usuario
    nuevo_usuario = Usuarios(nombre = usuario.nombre, 
                            correo = usuario.correo,
                            contraseña = usuario.contraseña)
    # Agregamos el nuevo usuario
    db.add(nuevo_usuario)
    db.commit() # Guardamos los cambios
    db.refresh(nuevo_usuario) # Refrescamos 
    return nuevo_usuario 

# Obtener todos los usuarios
def obtener_usuarios(db:Session):
    return db.query(Usuarios).all()

# Obtener un usuario por su id
def obtener_usuario_id(db:Session,usuario_id:int):
    return db.query(Usuarios).filter(Usuarios.id==usuario_id).first()
    

# _______________________________________Actividades____________________________________

# Crear actividades 
def crear_actividad(db:Session,actividad:Actividadescrear):
    nueva_actividad = Actividades(nombre_actividad = actividad.nombre_actividad,
                                descripcion = actividad.descripcion,
                                estado = actividad.estado,
                                Usuarios_id= actividad.Usuarios_id)
    db.add(nueva_actividad)
    db.commit()
    db.refresh(nueva_actividad)
    return nueva_actividad

# Obtenr todas las actividades por usuario
def obtener_actividades_por_usuario(db: Session, usuario_id: int):
    return db.query(Actividades).filter(Actividades.Usuarios_id == usuario_id).all()

def obtener_actividades(db: Session):
    return db.query(Actividades).all()

# Funcion para actualizar actividades
def actualizar_actividad(db: Session, actividad_id: int, datos_actualizados: ActividadesUsuarios):
    actividad = db.query(Actividades).filter(Actividades.id_actividad == actividad_id).first()
    if not actividad:
        return {"mensaje": "Actividad no encontrada"}
    
    actividad.nombre_actividad = datos_actualizados.nombre_actividad
    actividad.descripcion = datos_actualizados.descripcion
    actividad.estado = datos_actualizados.estado
    
    db.commit()
    db.refresh(actividad)
    
    return actividad

# Eliminar actividad 
def eliminar_actividad(db: Session, actividad_id: int):
    actividad = db.query(Actividades).filter(Actividades.id_actividad == actividad_id).first()
    if actividad:
        db.delete(actividad)
        db.commit()
        return {"mensaje": "Actividad eliminada correctamente"}
    else:
        return {"mensaje": "Actividad no encontrada"}
    
