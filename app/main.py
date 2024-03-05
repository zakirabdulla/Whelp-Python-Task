
from contextlib import asynccontextmanager
# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Own Imports
# from user import models as user_models
# from config.database import mongo_db

from .routers import api_v1_router
from .db import database

from core.models import User,Task




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the models
    database.connect()
    database.create_tables([User,Task])
    yield

app = FastAPI(title="Whelp Python Task", version="0.1.0",lifespan=lifespan)

app.include_router(api_v1_router, prefix="/api/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

