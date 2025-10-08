from fastapi import APIRouter, Depends
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload

from ..use_cases import drivers

router = APIRouter()

DRIVER_TAG = "drivers"



@router.get("/drivers/startWorkShift", tags=[DRIVER_TAG])
async def start_work_shift(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.start_work_shift(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.get("/drivers/stopWorkShift", tags=[DRIVER_TAG])
async def stop_work_shift(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.stop_work_shift(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.get("/drivers/acceptApplication", tags=[DRIVER_TAG])
async def accept_application(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.accept_application(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.get("/drivers/rejectApplication", tags=[DRIVER_TAG])
async def reject_application(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.reject_application(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.get("/drivers/all", tags=[DRIVER_TAG])
async def retrieve_all_drivers(causer: JWTPayload = Depends(get_jwt_payload)):
    res, err = drivers.retrieve_all(causer)
    if err is not None:
        return {"error": err}
    return {"response": res}
