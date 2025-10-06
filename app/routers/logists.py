
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, JWTPayload

from app.api_schemas.user_login_schema import LoginInfo
from app.api_schemas.user_driver_regist_schema import DriverRegistrInfo
from app.api_schemas.user_logist_registr_schema import LogistRegistrInfo


router = APIRouter()



@router.post("/logists/sendDriverApplication", tags=["logists"])
async def start_work_s(causer: JWTPayload = Depends(get_current_user)):
    return {"response": "success"}


