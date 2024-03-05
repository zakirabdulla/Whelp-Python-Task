from datetime import datetime, timedelta

from argon2 import PasswordHasher
import argon2

from peewee import DoesNotExist

from fastapi import HTTPException

from jose import JWTError, jwt

from app.config import settings

from .models import Task, User

ph = PasswordHasher()



class UserUseCase():

    def hash_password(self, password):
        return ph.hash(password)

    def create_user(self, user):
        hashed_password = self.hash_password(user.password)
        return User.create(username=user.username, password=hashed_password)
    
    def check_username(self, username):
        return User.select().where(User.username == username).exists()
    
    def get_user_by_username(self, username:str) -> User:
        return User.get(User.username == username)
    
    def authenticate(self,username:str,password:str):
        user = self.get_user_by_username(username)
        if not user:
            return None
        try:
            if not ph.verify(user.password, password):
                return None
        except argon2.exceptions.VerifyMismatchError:
            return None
        return user
    
    def create_access_token(self,user:User):
        to_encode = {
            "iss": user.id,
            "sub": "access_token"
        }
        
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self,user:User):
        to_encode = {
            "iss": user.id,
            "sub": "refresh_token"
        }
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def get_user_by_id(self, user_id:int) -> User:
        return User.get(User.id == user_id)
    
    def verify_refresh_token(self, token:str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except JWTError:
            return False
        if payload.get("sub") != "refresh_token":
            return False
        user_id = payload.get("iss")
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        return user


    def create_tokens(self,user:User):
        return {
            "access": self.create_access_token(user),
            "refresh": self.create_refresh_token(user)
        }

user_usecase = UserUseCase()



class TaskUseCase():

    def create_task(self, user:User, ip:str) -> Task:
        return Task.create(user=user, ip=ip)
    
    def get_user_task_by_id(self,user_id:int, task_id:int) -> Task:
        try:
            return Task.get(Task.id == task_id, Task.user == user_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Task not found")
    


task_usecase = TaskUseCase()
    
