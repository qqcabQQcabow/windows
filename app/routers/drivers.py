from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload, TrackForm, RoleEnum
from ..infrastructure.db import db_drivers

from ..use_cases import drivers

router = APIRouter()

DRIVER_TAG = "drivers"


@router.get("/drivers/profile", tags=[DRIVER_TAG])
async def retrieve_driver_profile(causer: JWTPayload = Depends(get_jwt_payload)):
    res, err = drivers.profile(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": res}


@router.get("/drivers/all", tags=[DRIVER_TAG])
async def retrieve_all_drivers(causer: JWTPayload = Depends(get_jwt_payload)):
    res, err = drivers.retrieve_all(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": res}


@router.get("/drivers/startWorkShift/{grz}", tags=[DRIVER_TAG])
async def start_work_shift(
    grz: str, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = drivers.start_work_shift(causer, grz)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.get("/drivers/stopWorkShift", tags=[DRIVER_TAG])
async def stop_work_shift(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.stop_work_shift(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.get("/drivers/workShiftsHistory", tags=[DRIVER_TAG])
async def retrieve_work_shifts_history(causer: JWTPayload = Depends(get_jwt_payload)):
    if not causer.login in [RoleEnum.DRIVER]:
        raise HTTPException(status_code=500, detail=str("Нет прав"))
    return {"response": db_drivers.retrieve_work_shifts_history(causer.login)}


@router.post("/drivers/acceptApplication", tags=[DRIVER_TAG])
async def accept_application(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.accept_application(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.post("/drivers/rejectApplication", tags=[DRIVER_TAG])
async def reject_application(causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.reject_application(causer)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.post("/drivers/addTrack", tags=[DRIVER_TAG])
async def add_track(data: TrackForm, causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.add_track(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.delete("/drivers/delTrack/{grz}", tags=[DRIVER_TAG])
async def del_track(grz: str, causer: JWTPayload = Depends(get_jwt_payload)):
    err = drivers.del_track(causer, grz)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.get("/drivers/allTrack", tags=[DRIVER_TAG])
async def retrieve_all_track(causer: JWTPayload = Depends(get_jwt_payload)):
    if not (causer.role in [RoleEnum.DRIVER]):
        raise HTTPException(status_code=500, detail=str("Нет прав"))
    return {"response": db_drivers.retrieve_tracks(causer.login)}
