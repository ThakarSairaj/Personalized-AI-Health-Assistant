# main.py
from fastapi import FastAPI
from database_con.database import base, engine
from controller.user_controller import router as user_router
from controller.health_basic_details_controller import router as health_router
from controller.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ only for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base.metadata.create_all(bind=engine)

app.include_router(user_router)

app.include_router(health_router)

app.include_router(auth_router)
