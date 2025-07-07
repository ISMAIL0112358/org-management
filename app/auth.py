from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt

SECRET_KEY = "your_jwt_secret"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    return jwt.encode(data.copy(), SECRET_KEY, algorithm="HS256")

def get_current_master_admin(token: str = Depends(OAuth2PasswordBearer(tokenUrl="master/login"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        role: str = payload.get("role")
        if role is None or role != "master_admin":
            raise credentials_exception
        return payload
    except jwt.PyJWTError:
        raise credentials_exception
