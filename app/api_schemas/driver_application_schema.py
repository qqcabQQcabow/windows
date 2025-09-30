from pydantic import BaseModel
from enum import Enum

class ContainerType(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class DriverApplication(BaseModel):
    # id: int
    submission_time: int
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
