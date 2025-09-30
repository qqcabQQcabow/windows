from fastapi import APIRouter
from app.api_schemas.user_login_schema import LoginInfo
import app.infrastructure.auth_utils as auth_u

router = APIRouter()

@router.post("/users/login", tags=["users"])
async def login_to_system(data: LoginInfo):
    # check password valid
    return {"token": auth_u.create_jwt_token(data.login, "ADMIN" )}
