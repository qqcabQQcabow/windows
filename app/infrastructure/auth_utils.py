import jwt
import time
from enum import Enum

from pydantic import BaseModel

SECRET_KEY = "AladinGalendaGubin-AGG-GAG-GGA"
ALGORITHM = "HS256"
LIFE_TIME_SEC = 24*3600*30


class RoleEnum(str, Enum):
    DRIVER = "DRIVER"
    LOGIST = "LOGIST"
    ADMIN = "ADMIN"


class JWTPayload(BaseModel):
    login: str
    role: RoleEnum
    exp: int

    @classmethod
    def create(cls, login: str, role: RoleEnum, lifetime_sec: int = 3600):
        return cls(
            login=login,
            role=role,
            exp=int(time.time()) + lifetime_sec
        )


def create_jwt_token(login: str, role: RoleEnum) -> str:
    return jwt.encode(JWTPayload.create(login, role, LIFE_TIME_SEC).model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token:str) -> JWTPayload:
    decod = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return JWTPayload(**decod)
