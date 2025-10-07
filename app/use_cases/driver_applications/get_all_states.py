from ...infrastructure.auth_utils import JWTPayload, RoleEnum
from ...infrastructure.db.driver_applications import retrieve_all_states, contains_driver, contains_logist

from typing import Optional, Tuple, Any

def retrieve_all_da_states(causer: JWTPayload, application_id: int) -> Tuple[list[dict[Any, Any]], Optional[str]]:
    try:
        if causer.role == RoleEnum.LOGIST and not contains_logist(application_id, causer.login):
            return [], f"Нет доступа"
        if causer.role == RoleEnum.DRIVER and not contains_driver(application_id, causer.login):
            return [], f"Нет доступа"

        return retrieve_all_states(application_id), None
    except Exception as e:
        return [], f"Ошикбка. {e}"

