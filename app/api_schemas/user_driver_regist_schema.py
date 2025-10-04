from pydantic import BaseModel

class DriverRegistrInfo(BaseModel):

    login: str
    password: str

    phone: str
    email: str

    name: str
    surname: str
    patronymic: str

    born_date: int

    passport_numbers: str
    driver_license_numbers: str

    job_license_numbers: str
    snils_numbers: str
