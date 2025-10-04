from pydantic import BaseModel

class LogistRegistrInfo(BaseModel):

    login: str
    password: str

    phone: str
    email: str

    name: str
    surname: str
    patronymic: str

    born_date: int
