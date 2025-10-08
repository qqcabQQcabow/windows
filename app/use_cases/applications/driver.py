from ...infrastructure.db.driver_applications import change_driver
from ...infrastructure.auth_utils import RoleEnum, JWTPayload
from ...api_schemas.driver_application_schema import ChangeApplicationDriver
from typing import Optional

def change(causer: JWTPayload, data: ChangeApplicationDriver) -> Optional[str]:
    try:
        if causer.role != RoleEnum.LOGIST:
            return f"Только логист может изменить статус заявки"

        success = change_driver(data.application_id, data.new_driver_login)
        if not success:
            return f"Не удалось изменить водителя"

        return None
    except Exception as e:
        return f"Ошибка. {e}"
