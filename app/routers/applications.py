from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload

from ..infrastructure.data_schemas import (
    Application,
    ApplicationState,
    ChangeApplicationDriver,
    ApplicationId,
    RoleEnum,
)


from ..infrastructure.db import db_applications

from ..use_cases import applications


router = APIRouter()

DA_TAG = "driver_applications"


@router.post("/applications/create", tags=[DA_TAG])
async def create_application(
    data: Application, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = applications.create(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))

    return {"response": "success"}


@router.delete("/applications/delete/{id}", tags=[DA_TAG])
async def delete_application(id: int, causer: JWTPayload = Depends(get_jwt_payload)):
    err = applications.delete(causer, id)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))

    return {"response": "success"}


@router.put("/applications/initState", tags=[DA_TAG])
async def init_application_state(
    data: ApplicationState, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = applications.init_state(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.put("/applications/outState", tags=[DA_TAG])
async def out_application_state(
    data: ApplicationState, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = applications.out_state(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}


@router.get("/applications/all", tags=[DA_TAG])
async def retrieve_all(causer: JWTPayload = Depends(get_jwt_payload)):
    return {"response": db_applications.retrieve_all(causer)}


@router.get("/applications/allNew", tags=[DA_TAG])
async def retrieve_all_new(causer: JWTPayload = Depends(get_jwt_payload)):
    if causer.role == RoleEnum.LOGIST:
        return {"response": db_applications.retrieve_all_new_for_logist(causer.login)}

    raise HTTPException(status_code=500, detail=str("Нет прав"))


@router.get("/applications/allInProcess", tags=[DA_TAG])
async def retrieve_all_in_process(causer: JWTPayload = Depends(get_jwt_payload)):
    if causer.role == RoleEnum.LOGIST:
        return {
            "response": db_applications.retrieve_all_in_process_for_logist(causer.login)
        }

    raise HTTPException(status_code=500, detail=str("Нет прав"))


@router.get("/applications/allCompleted", tags=[DA_TAG])
async def retrieve_all_completed(causer: JWTPayload = Depends(get_jwt_payload)):
    if causer.role == RoleEnum.LOGIST:
        return {
            "response": db_applications.retrieve_all_completed_for_logist(causer.login)
        }

    raise HTTPException(status_code=500, detail=str("Нет прав"))


@router.get("/applications/allStates/{id}", tags=[DA_TAG])
async def retrieve_all_states(id: int, causer: JWTPayload = Depends(get_jwt_payload)):
    res, err = applications.retrieve_all_states(causer, id)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": res}


@router.put("/applications/changeDriver", tags=[DA_TAG])
async def change_application_driver(
    data: ChangeApplicationDriver, causer: JWTPayload = Depends(get_jwt_payload)
):
    err = applications.change_driver(causer, data)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"response": "success"}
