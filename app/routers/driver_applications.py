from fastapi import APIRouter, Depends
from app.api_schemas.driver_application_schema import DriverApplication, DriverApplicationState
from app.dependencies import get_current_user, JWTPayload

from ..use_cases.driver_applications import get_all, create, change_state

router = APIRouter()

@router.post("/driverApplications/create", tags=["driver_applications"])
async def create_driver_app(drive_app: DriverApplication, causer: JWTPayload = Depends(get_current_user)):
    err = create.create_da(causer, drive_app)
    if err is not None:
        return {"error", err}

    return {"response": "success"}

@router.post("/driverApplications/initState", tags=["driver_applications"])
async def init_da_state(drive_app: DriverApplicationState, causer: JWTPayload = Depends(get_current_user)):
    err = change_state.init_state_use_case(causer, drive_app)
    if err is not None:
        return {"error", err}
    return {"response": "success"}

@router.post("/driverApplications/outState", tags=["driver_applications"])
async def out_da_state(drive_app: DriverApplicationState, causer: JWTPayload = Depends(get_current_user)):
    err = change_state.out_state_use_case(causer, drive_app)
    if err is not None:
        return {"error", err}
    return {"response": "success"}

@router.get("/driverApplications/all", tags=["driver_applications"])
async def retrieve_all(causer: JWTPayload = Depends(get_current_user)):
    if causer.role == "LOGIST":
        return {"response": get_all.get_all_driver_applications_for_logist(causer.login)}
    if causer.role == "DRIVER":
        return {"response": get_all.get_all_driver_applications_for_driver(causer.login)}

    return {"error": "undefined role"}

