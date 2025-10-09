from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload

from ..infrastructure.data_schemas import SendApplication, RateDriverForm
from ..use_cases import logists


router = APIRouter()

LOGIST_TAG = "logists"


@router.post("/logists/rateDriver", tags=[LOGIST_TAG])
async def rate_driver(data: RateDriverForm, causer: JWTPayload = Depends(get_jwt_payload)):
    err = logists.rate(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}

@router.get("/logists/profile", tags=[LOGIST_TAG])
async def retrieve_logist_profile(causer: JWTPayload = Depends(get_jwt_payload)):
    res, err = logists.profile(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": res}


@router.post("/logists/sendApplicationToDriver", tags=[LOGIST_TAG])
async def send_application_to_driver(
    data: SendApplication, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = logists.send_application_to_driver(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}
