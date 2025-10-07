from ...infrastructure.db.drivers import retrieve_all_drivers
from ...infrastructure.auth_utils import JWTPayload, RoleEnum

from typing import Tuple, Any, Optional

def get_all_drivers(causer: JWTPayload) -> Tuple[list[dict[Any, Any]], Optional[str]]:
    try:
        if causer.login == RoleEnum.DRIVER:
            return [], f"Нет прав"
        res = retrieve_all_drivers()
        return res, None
    except Exception as e:
        return [], f"Обнаружена ошибка {e}"
