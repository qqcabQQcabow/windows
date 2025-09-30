import jwt
import time

from pydantic import BaseModel

SECRET_KEY = "AladinGalendaGubin-AGG-GAG-GGA"
ALGORITHM = "HS256"
LIFE_TIME_SEC = 10


class JWTPayload(BaseModel):
    login: str
    role: str
    exp: int

    @classmethod
    def create(cls, login: str, role: str, lifetime_sec: int = 3600):
        return cls(
            login=login,
            role=role,
            exp=int(time.time()) + lifetime_sec
        )


def create_jwt_token(login: str, role: str) -> str:
    return jwt.encode(JWTPayload.create(login, role, LIFE_TIME_SEC).model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token:str) -> JWTPayload:
    decod = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return JWTPayload(**decod)
