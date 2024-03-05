from fastapi import APIRouter

from core.api import router as core_router



api_v1_router = APIRouter(tags=["v1"])

api_v1_router.include_router(core_router, prefix="")


