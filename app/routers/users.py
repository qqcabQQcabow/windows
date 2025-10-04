from fastapi import APIRouter
from app.api_schemas.user_login_schema import LoginInfo
from app.api_schemas.user_driver_regist_schema import DriverRegistrInfo
from app.api_schemas.user_logist_registr_schema import LogistRegistrInfo
import app.infrastructure.auth_utils as auth_u

from ..use_cases.users.regist import execute_registr_driver
from ..use_cases.users.regist import execute_registr_logits
from ..use_cases.users.log_in import execute_log_in

router = APIRouter()

@router.post("/users/login", tags=["users"])
async def login_to_system(data: LoginInfo):
    token, err = execute_log_in(data)
    if err is not None:
        return {"error": err}

    return {"token": token}




@router.post("/users/registrDriver", tags=["users"])
async def registr_driver(data: DriverRegistrInfo):
    err = execute_registr_driver(data)
    if err is not None:
        return {"error": err}
    return {"response": "success"}





@router.post("/users/registrLogist", tags=["users"])
async def registr_logist(data: LogistRegistrInfo):
    err = execute_registr_logits(data)
    if err is not None:
        return {"error": err}
    return {"response": "success"}
