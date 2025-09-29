import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.simulation import Simulation
from models.user import User
from models.file import File
from models.access_control import AccessControl
from models.request import Request
from models.constants import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulation = Simulation()


@app.get("/get_logs")
def get_logs():
    return simulation.informs.get_all_logs()

@app.get("/get_users")
def get_users():
    return simulation.get_all_users()

@app.post("/add_user")
def add_user(user: dict):
    user = User(len(simulation.users) + 1, **user)
    simulation.add_user(user)
    return {"message": "Usuario agregado exitosamente."}

@app.post("/edit_user/{user_id}")
def edit_user(user_id: int, updated_user: dict):
    updated_user = User(**updated_user)
    simulation.edit_user(user_id, updated_user)
    return {"message": "Usuario modificado exitosamente."}

@app.get("/get_files")
def get_files():
    return simulation.get_all_files()

@app.post("/add_file")
def add_file(file: dict):
    file = File(len(simulation.files) + 1, **file)
    simulation.add_file(file)
    return {"message": "Archivo agregado exitosamente."}

@app.post("/edit_file/{file_id}")
def edit_file(file_id: int, updated_file: dict):
    updated_file = File(**updated_file)
    simulation.edit_file(file_id, updated_file)
    return {"message": "Archivo modificado exitosamente."}

@app.post("/run_simulation")
def run_simulation():
    simulation.run_simulation()
    return {"message": "Simulación ejecutada exitosamente."}

@app.post("/run_action")
def run_action(request: dict):
    request = Request(**request)
    user = next((u for u in simulation.users if u.id == request.user_id), None)
    file = next((f for f in simulation.files if f.id == request.file_id), None)

    if not user or not file:
        raise HTTPException(status_code=404, detail="Usuario o archivo no encontrado.")

    result, message = AccessControl().check_permissions(
        model=request.model,
        role=user.role,
        resource_level=file.resource_level,
        action=request.action
    )

    simulation.informs.log_access_attempt(
        model=request.model,
        user=user,
        file=file,
        action=request.action,
        result=result,
        message=message
    )

    return {
        "result": result,
        "message": message
    }