from fastapi import APIRouter, Depends
from app.api_schemas.driver_application_schema import DriverApplication, DriverApplicationState, ChangeApplicationDriver
from app.dependencies import get_current_user, JWTPayload
from ..infrastructure.auth_utils import RoleEnum

from ..use_cases.driver_applications import get_all, create, change_state, change_driver, get_all_states
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



@router.get("/driverApplications/all", tags=[DA_TAG])
async def retrieve_all(causer: JWTPayload = Depends(get_current_user)):
    if causer.role == RoleEnum.LOGIST:
        return {"response": get_all.get_all_driver_applications_for_logist(causer.login)}
    if causer.role == RoleEnum.DRIVER:
        return {"response": get_all.get_all_driver_applications_for_driver(causer.login)}

    return {"error": "undefined role"}

@router.get("/driverApplications/allStates/{id}", tags=[DA_TAG])
async def retrieve_all_states(id: int, causer: JWTPayload = Depends(get_current_user)):
    res, err = get_all_states.retrieve_all_da_states(causer, id)
    if err is not None:
        return {"error": err}
    return {"response": res}


@router.post("/driverApplications/changeDriver", tags=[DA_TAG])
async def change_da_driver(data: ChangeApplicationDriver, causer: JWTPayload = Depends(get_current_user)):
    err = change_driver.change_driver_application_driver(causer, data)
    if err is not None:
        return {"error": err}
    return {"response": "success"}
