from fastapi import FastAPI

from app.routers import users, drivers, logists, applications

app = FastAPI()
app.include_router(applications.router)
app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(logists.router)


@app.get("/")
async def root():
    return {"message": "Hello logit!"}
