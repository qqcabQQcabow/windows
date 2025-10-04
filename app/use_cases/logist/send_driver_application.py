from ...infrastructure.db.driver_applications import start_await
from ...infrastructure.db.users import get_user
from ...infrastructure.auth_utils import JWTPayload

from typing import Optional

def send_application_to_driver(causer: JWTPayload, driver_login: str) -> Optional[str]:
    try:
        driver = get_user(driver_login)
        if driver is None:
            return f"Водитель с логином {driver_login} не найден"

    except Exception as e:
        return f"Обнаружена ошибка. {e}"
