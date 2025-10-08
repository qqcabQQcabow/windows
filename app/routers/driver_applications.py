from fastapi import APIRouter, Depends
from app.api_schemas.driver_application_schema import DriverApplication, DriverApplicationState, ChangeApplicationDriver, ApplicationId
from app.dependencies import get_current_user, JWTPayload
from ..infrastructure.auth_utils import RoleEnum

from ..infrastructure.db import driver_applications

from ..use_cases.driver_applications import create, change_state, change_driver, get_all_states
router = APIRouter()

DA_TAG = "driver_applications"

@router.post("/driverApplications/create", tags=[DA_TAG])
async def create_driver_app(drive_app: DriverApplication, causer: JWTPayload = Depends(get_current_user)):
    err = create.create_da(causer, drive_app)
    if err is not None:
        return {"error": err}

    return {"response": "success"}




@router.post("/driverApplications/initState", tags=[DA_TAG])
async def init_da_state(drive_app: DriverApplicationState, causer: JWTPayload = Depends(get_current_user)):
    err = change_state.init_state_use_case(causer, drive_app)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.post("/driverApplications/outState", tags=[DA_TAG])
async def out_da_state(drive_app: DriverApplicationState, causer: JWTPayload = Depends(get_current_user)):
    err = change_state.out_state_use_case(causer, drive_app)
    if err is not None:
        return {"error": err}
    return {"response": "success"}




@router.get("/driverApplications/allNew", tags=[DA_TAG])
async def retrieve_all_new(causer: JWTPayload = Depends(get_current_user)):
    if causer.role == RoleEnum.LOGIST:
        return {"response": driver_applications.retrieve_all_new_for_logist(causer.login)}

    return {"error": "Нет прав"}




@router.get("/driverApplications/allCompleted", tags=[DA_TAG])
async def retrieve_all_completed(causer: JWTPayload = Depends(get_current_user)):
    if causer.role == RoleEnum.LOGIST:
        return {"response": driver_applications.retrieve_all_completed_for_logist(causer.login)}

    return {"error": "Нет прав"}




@router.get("/driverApplications/all", tags=[DA_TAG])
async def retrieve_all(causer: JWTPayload = Depends(get_current_user)):
    return {"response": driver_applications.retrieve_all(causer)}



@router.post("/driverApplications/allStates", tags=[DA_TAG])
async def retrieve_all_states(data: ApplicationId, causer: JWTPayload = Depends(get_current_user)):
    res, err = get_all_states.retrieve_all_da_states(causer, data.application_id)
    if err is not None:
        return {"error": err}
    return {"response": res}




@router.post("/driverApplications/changeDriver", tags=[DA_TAG])
async def change_da_driver(data: ChangeApplicationDriver, causer: JWTPayload = Depends(get_current_user)):
    err = change_driver.change_driver_application_driver(causer, data)
    if err is not None:
        return {"error": err}
    return {"response": "success"}
