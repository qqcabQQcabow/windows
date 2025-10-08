from pydantic import BaseModel
from enum import Enum
import time

class ContainerType(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Application(BaseModel):
    container_type: ContainerType
    container_count: int
    container_submission_time: int
    container_loading_address: str
    loading_contact_full_name: str
    loading_contact_phone: str
    shipper_name: str
    shipper_address: str
    cargo_name: str
    cargo_package_count: int
    cargo_weight: int
    departure_station_name: str
    destination_station_name: str
    consignee_name: str
    consignee_address: str
    unloading_contact_full_name: str
    unloading_contact_phone: str
    notes: str

class ApplicationStateEnum(str, Enum):
   APPLICATION           ='APPLICATION'
   TERMINAL              ='TERMINAL'
   WAREHOUSE             ='WAREHOUSE'
   DEPARTURE_STATION     ='DEPARTURE_STATION'
   DESTINATION_STATION   ='DESTINATION_STATION'
   CARGO_DELIVERY        ='CARGO_DELIVERY'
   EMPTY_CONTAINER_RETURN='EMPTY_CONTAINER_RETURN'


class ApplicationState(BaseModel):
    application_id: int
    state_name: ApplicationStateEnum


class SendApplication(BaseModel):
    application_id: int
    driver_login: str

class ChangeApplicationDriver(BaseModel):
    application_id: int
    new_driver_login: str

class ApplicationId(BaseModel):
    application_id: int

#----------------------------------------------------------------------------------


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


#----------------------------------------------------------------------------------

class LoginInfo(BaseModel):
    login: str
    password: str


#------------------------------------------------------------------------------------

class LogistRegistrInfo(BaseModel):

    login: str
    password: str

    phone: str
    email: str

    name: str
    surname: str
    patronymic: str

    born_date: int


#----------------------------------------------------------------------------------

class RoleEnum(str, Enum):
    DRIVER = "DRIVER"
    LOGIST = "LOGIST"
    ADMIN = "ADMIN"


class JWTPayload(BaseModel):
    login: str
    role: RoleEnum
    exp: int

    @classmethod
    def create(cls, login: str, role: RoleEnum, lifetime_sec: int = 3600):
        return cls(
            login=login,
            role=role,
            exp=int(time.time()) + lifetime_sec
        )


#-----------------------------------------------------------------------------------

class SendMessageForm(BaseModel):
    recepient_login: str
    message: str

class ReceiptLogin(BaseModel):
    recepient_login: str

#========================================================================================

class TrackForm(BaseModel):
    grz: str
    brand: str
    color: str
    model: str


class TrackGrz(BaseModel):
    grz: str
