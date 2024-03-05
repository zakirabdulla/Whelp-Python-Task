from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt

from .usecases import user_usecase

from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/")



def get_current_user(*,token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise credentials_exception
    user_id: str = payload.get("iss")
    sub:str = payload.get("sub")
    if user_id is None or sub != "access_token":
        raise credentials_exception
        
    user = user_usecase.get_user_by_id(user_id=user_id)
    if user is None:
        raise credentials_exception
    return user