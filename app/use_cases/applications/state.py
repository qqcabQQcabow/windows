
from ...api_schemas.driver_application_schema import DriverApplicationState
from ...infrastructure.auth_utils import JWTPayload, RoleEnum
from ...infrastructure.db.driver_applications import init_driver_state, out_driver_state

from typing import Optional



def init(causer: JWTPayload, new_state: DriverApplicationState) -> Optional[str]:
    try:

        if causer.role != RoleEnum.DRIVER:
            return "Только водитель может изменить состояние заявки"

        success = init_driver_state(new_state)
        if not success:
            return "Не удалось изменить состояние заявки"

        return None
    except Exception as e:
        return f"Ошибка. {e}"



def out(causer: JWTPayload, new_state: DriverApplicationState) -> Optional[str]:
    try:

        if causer.role != RoleEnum.DRIVER:
            return "Только водитель может изменить состояние заявки"

        success = out_driver_state(new_state)
        if not success:
            return "Не удалось изменить состояние заявки"

        return None
    except Exception as e:
        return f"Ошибка. {e}"
