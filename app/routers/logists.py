from fastapi import APIRouter, Depends
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload

from ..infrastructure.data_schemas import SendApplication
from ..use_cases import logists


router = APIRouter()

LOGIST_TAG = "logists"


@router.post("/logists/sendApplicationToDriver", tags=[LOGIST_TAG])
async def send_application_to_driver(data: SendApplication, causer: JWTPayload = Depends(get_jwt_payload)):
    err = logists.send_application_to_driver(causer, data)
    if err is not None:
        return {"error": err}
    return {"response": "success"}
