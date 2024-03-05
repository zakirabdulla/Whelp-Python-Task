from typing import Annotated, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .models import Task, User

from .deps import get_current_user

from .schemas import (
    SignupSchema,
    UserResponseSchema,
    TokensSchema,
    ObtainAccessTokenSchema,
    AccessTokenSchema,
    TaskCreate,
    TaskCreateResponse,
    StatusResponse,
)

from .usecases import user_usecase, task_usecase

router = APIRouter(tags=["core"])

@router.post("/signup/")
def create_user(user: SignupSchema) -> UserResponseSchema:
    if user_usecase.check_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = user_usecase.create_user(user)
    return UserResponseSchema(username=user.username,
                                id=user.id, 
                                created_at=user.created_at.isoformat()
                            )

@router.post("/auth/")
def login(*,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokensSchema:
    user = user_usecase.authenticate(form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return user_usecase.create_tokens(user)

@router.get("/user/")
def me(current_user: User = Depends(get_current_user)) -> UserResponseSchema:
    return current_user


@router.post("/refresh/")
def obtain_token(*,token: ObtainAccessTokenSchema) -> AccessTokenSchema:
    user = user_usecase.verify_refresh_token(token.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token =  user_usecase.create_access_token(user)
    return {"access":access_token}



from celery_tasks.tasks import add, fetch_ip_data

@router.post("/test/")
def test():
    task = fetch_ip_data.apply_async(args=["0.0.0.0"])
    return {"task_id":task.id}

@router.post("/task/")
def create_task(*,current_user: User = Depends(get_current_user),data:TaskCreate) -> TaskCreateResponse:
    str_ip = str(data.ip)
    task = task_usecase.create_task(current_user,str_ip)
    celery_task = fetch_ip_data.apply_async(args=[task.id])
    task.uid = str(celery_task.id)
    task.save()
    return {"id":task.id}

@router.get("/status/{id}")
def get_task(*,id:int,current_user: User = Depends(get_current_user)) -> StatusResponse:
    task = task_usecase.get_user_task_by_id(current_user.id,id)
    return task
