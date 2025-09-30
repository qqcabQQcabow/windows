from pydantic import BaseModel

class LoginInfo(BaseModel):
    login: str
    password: str
