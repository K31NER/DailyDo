from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import engine, Base, sessionLocal
from sqlalchemy.orm import Session
import uvicorn
import schemas
import crud
from typing import List

templates = Jinja2Templates(directory="templates")


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
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Frontend"], response_model=None, description="Sirve la página principal HTML.")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ________________________________________Usuarios_____________________________________

@app.post("/users/",tags=["Users"],response_model=schemas.Usuariobase, description= "Crea un nuevo usuario en la base de datos. Recibe los datos del usuario como entrada y devuelve la información del usuario creado.")
def crear_usuario_endpoint(usuario: schemas.Crearusuario, db:Session= Depends(get_db)):
    return crud.crear_usuario(db = db, usuario=usuario)

# ________________________________________Actividades_____________________________________

@app.post("/api/actividades/",tags=["Actividades API"],response_model=schemas.Actividadesbase, description = "Crea una nueva actividad en la base de datos. Recibe los datos de la actividad como entrada y devuelve la información de la actividad creada.")
def crear_actividad_endpoint(actividad: schemas.Actividadescrear, db:Session= Depends(get_db)):
    new_activity = crud.crear_actividad(db = db, actividad= actividad)
    return new_activity

@app.get("/api/actividades/", response_model=List[schemas.ActividadesUsuarios],tags=["Actividades API"], description= "Obtiene una lista de todas las actividades registradas en la base de datos.")
def obtener_actividades_endpoint(db: Session = Depends(get_db)):
    actividades = crud.obtener_actividades(db)
    return actividades

@app.put("/api/actividades/{actividad_id}", response_model=schemas.ActividadesUsuarios,tags=["Actividades API"], description= "Actualiza la información de una actividad existente utilizando su ID. Recibe los nuevos datos de la actividad y devuelve la actividad actualizada.")
def actualizar_actividad_endpoint(actividad_id: int, datos: schemas.Actividadescrear, db: Session = Depends(get_db)):
    updated_activity = crud.actualizar_actividad(db=db, actividad_id=actividad_id, datos_actualizados=datos)
    if isinstance(updated_activity, dict) and "mensaje" in updated_activity:
         raise HTTPException(status_code=404, detail=updated_activity["mensaje"])
    return updated_activity


@app.delete("/api/actividades/{actividad_id}",tags=["Actividades API"], description= "Elimina una actividad de la base de datos utilizando su ID.")
def eliminar_actividad_endpoint(actividad_id: int, db: Session = Depends(get_db)):
    resultado = crud.eliminar_actividad(db=db, actividad_id=actividad_id)
    if resultado.get("mensaje") == "Actividad no encontrada":
         raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return resultado


if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",reload=True, port=8000)