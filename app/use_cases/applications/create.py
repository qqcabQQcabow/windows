from ...api_schemas.driver_application_schema import DriverApplication
from ...infrastructure.auth_utils import JWTPayload
from ...infrastructure.db.driver_applications import create_driver_application

from typing import Optional

def create_da(causer: JWTPayload, data: DriverApplication) -> Optional[str]:
    '''
    Return None if success
    Return Err reason, if bad
    '''

    try:
        if causer.role != "LOGIST":
            return "Нет прав"
        
        create_driver_application(causer.login, data)

        return None


    except Exception as e:
        return f"Ошибка. {e}"

