from fastapi import FastAPI,Depends,HTTPException
from database import engine,Base, sessionLocal
from models import Actividades,Usuarios
from sqlalchemy.orm import Session
import uvicorn
import schemas
import crud

# Obtener la base de datos
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Crear las tablas
Base.metadata.create_all(bind= engine)

# Inicalizamos la app
app = FastAPI(title="DailyDo" , version="1.0")

# ________________________________________Usuarios_____________________________________

@app.post("/users/",tags=["Users"],response_model=schemas.Usuariobase, description= "Crea un nuevo usuario en la base de datos. Recibe los datos del usuario como entrada y devuelve la información del usuario creado.")
def crear_usuario(usurio: schemas.Crearusuario, db:Session= Depends(get_db)):
    return crud.crear_usuario(db = db, usuario=usurio)

# ________________________________________Actividades_____________________________________

@app.post("/actividades/",tags=["Actividades"],response_model=schemas.Actividadesbase, description = "Crea una nueva actividad en la base de datos. Recibe los datos de la actividad como entrada y devuelve la información de la actividad creada.")
def crear_actividades(actividad: schemas.Actividadescrear, db:Session= Depends(get_db)):
    return crud.crear_actividad(db = db, actividad= actividad)

@app.get("/actividades/", response_model=list[schemas.Actividadesbase],tags=["Actividades"], description= "Obtiene una lista de todas las actividades registradas en la base de datos.")
def obtener_actividades(db: Session = Depends(get_db)):
    return crud.obtener_actividades(db)

@app.put("/actividades/{actividad_id}", response_model=schemas.Actividadesbase,tags=["Actividades"], description= "Actualiza la información de una actividad existente utilizando su ID. Recibe los nuevos datos de la actividad y devuelve la actividad actualizada.")
def actualizar_actividad(actividad_id: int, datos: schemas.Actividadescrear, db: Session = Depends(get_db)):
    return crud.actualizar_actividad(db=db, actividad_id=actividad_id, datos_actualizados=datos)

@app.delete("/actividades/{actividad_id}",tags=["Actividades"], description= "Elimina una actividad de la base de datos utilizando su ID. Si la actividad no existe, se puede devolver un error indicando que no fue encontrada.")
def eliminar_actividad(actividad_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_actividad(db=db, actividad_id=actividad_id)

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",reload=True, port=8000)