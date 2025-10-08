import jwt
from .data_schemas import JWTPayload, RoleEnum


SECRET_KEY = "AladinGalendaGubin-AGG-GAG-GGA"
ALGORITHM = "HS256"
LIFE_TIME_SEC = 24*3600*30


def create_jwt_token(login: str, role: RoleEnum) -> str:
    return jwt.encode(JWTPayload.create(login, role, LIFE_TIME_SEC).model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token:str) -> JWTPayload:
    decod = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return JWTPayload(**decod)
