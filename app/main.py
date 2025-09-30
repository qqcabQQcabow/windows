from fastapi import Depends, FastAPI

from app.dependencies import get_current_user
from app.routers import driver_applications
from app.routers import users
from app.routers import drivers
from app.routers import logists

# app = FastAPI(dependencies=[Depends(get_current_user)])
app = FastAPI()
app.include_router(driver_applications.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello logit!"}
