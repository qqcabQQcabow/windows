
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, JWTPayload

from ..api_schemas.driver_application_schema import SendDriverApplication
from ..use_cases.logist.send_driver_application import send_application_to_driver


router = APIRouter()



@router.post("/logists/sendDriverApplication", tags=["logists"])
async def send_da_to_driver(data: SendDriverApplication, causer: JWTPayload = Depends(get_current_user)):
    err = send_application_to_driver(causer, data)
    if err is not None:
        return {"error": err}


    return {"response": "success"}


