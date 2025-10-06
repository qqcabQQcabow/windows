from fastapi import Depends, FastAPI

from app.dependencies import get_current_user
from app.routers import users, drivers, logists, driver_applications

app = FastAPI()
app.include_router(driver_applications.router)
app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(logists.router)


@app.get("/")
async def root():
    return {"message": "Hello logit!"}
