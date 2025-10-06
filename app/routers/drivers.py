from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, JWTPayload

from ..use_cases.drivers import work_shifts, handle_application


router = APIRouter()



@router.get("/drivers/startWorkShift", tags=["drivers"])
async def start_work_s(causer: JWTPayload = Depends(get_current_user)):
    err = work_shifts.start_driver_work_shift_use_case(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}

@router.get("/drivers/stopWorkShift", tags=["drivers"])
async def stop_work_s(causer: JWTPayload = Depends(get_current_user)):
    err = work_shifts.end_driver_work_shift_use_case(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}

@router.get("/drivers/acceptDA", tags=["drivers"])
async def accept_da(causer: JWTPayload = Depends(get_current_user)):
    err = handle_application.accept(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}

@router.get("/drivers/rejectDA", tags=["drivers"])
async def reject_da(causer: JWTPayload = Depends(get_current_user)):
    err = handle_application.reject(causer)
    if err is not None:
        return {"error": err}
    return {"response": "success"}
