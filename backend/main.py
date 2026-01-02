# main.py
from fastapi import FastAPI
from database_con.database import base, engine
from controller.user_controller import router as user_router
from controller.health_basic_details_controller import router as health_router

app=FastAPI()

base.metadata.create_all(bind=engine)

app.include_router(user_router)

app.include_router(health_router)