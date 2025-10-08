from fastapi import APIRouter, HTTPException

from ..use_cases import users
from ..infrastructure.data_schemas import LoginInfo, DriverRegistrInfo, LogistRegistrInfo

router = APIRouter()

USER_TAG = "users"

@router.post("/users/login", tags=[USER_TAG])
async def login_to_system(data: LoginInfo):
    token, err = users.log_in(data)
    if err is not None:
        HTTPException(status_code=500, detail=str(err))
    return {"token": token}




@router.post("/users/registrDriver", tags=[USER_TAG])
async def registr_driver(data: DriverRegistrInfo):
    err = users.registr_driver(data)
    if err is not None:
        HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}




@router.post("/users/registrLogist", tags=[USER_TAG])
async def registr_logist(data: LogistRegistrInfo):
    err = users.registr_logits(data)
    if err is not None:
        HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}
