from fastapi import APIRouter, Depends
from app.api_schemas.driver_application_schema import DriverApplication
from app.dependencies import get_current_user, JWTPayload

router = APIRouter()

@router.post("/driverApplications/registr", tags=["driver_applications"])
async def registr_DA(drive_app: DriverApplication, causer: JWTPayload = Depends(get_current_user)):
    return {"causer": causer.model_dump()}


@router.get("/driverApplications/all", tags=["driver_applications"])
async def retrieve_all():
    return {"status": "in_work"}
