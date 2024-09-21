# import jwt
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel

# SECRET_KEY = "SECRET"
# ALGORITHM = "HS256"

# from datetime import datetime, timedelta, timezone
# from typing import Annotated

# import jwt
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
# from pydantic import BaseModel

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def create_jwt_token(data: dict):
#     token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
#     return token

# def decode_jwt_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=403, detail="Invalid token")
