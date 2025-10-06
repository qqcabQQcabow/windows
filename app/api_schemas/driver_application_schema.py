from pydantic import BaseModel
from enum import Enum

class ContainerType(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"



class DriverApplication(BaseModel):
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

class DriverApplicationStateType(str, Enum):
   APPLICATION           ='APPLICATION'
   TERMINAL              ='TERMINAL'
   WAREHOUSE             ='WAREHOUSE'
   DEPARTURE_STATION     ='DEPARTURE_STATION'
   DESTINATION_STATION   ='DESTINATION_STATION'
   CARGO_DELIVERY        ='CARGO_DELIVERY'
   EMPTY_CONTAINER_RETURN='EMPTY_CONTAINER_RETURN'


class DriverApplicationState(BaseModel):
    application_id: int
    state_name: DriverApplicationStateType


class SendDriverApplication(BaseModel):
    application_id: int
    driver_login: str
