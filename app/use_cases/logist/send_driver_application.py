from ...infrastructure.db.driver_applications import start_await, get_current_state
from ...infrastructure.db.drivers import driver_at_work
from ...infrastructure.db.users import get_user
from ...infrastructure.auth_utils import JWTPayload
from ...api_schemas.driver_application_schema import SendDriverApplication, DriverApplicationStateType

from typing import Optional

def send_application_to_driver(causer: JWTPayload, data: SendDriverApplication) -> Optional[str]:
    try:
        if causer.role != "LOGIST":
            return f"Нет прав"

        da_state = get_current_state(data.application_id)
        if da_state is None:
            return f"Не удалось получить статус заявки"

        if da_state["state_name"] != DriverApplicationStateType.APPLICATION:
            return f"Отправить можно только созданную заявку"

        driver = get_user(data.driver_login)
        if driver is None:
            return f"Водитель с логином {data.driver_login} не найден"
        
        if not driver_at_work(data.driver_login):
            return f"Водитель не на работе"

        if not start_await(data.application_id, data.driver_login):
            return f"Не удалось отправить заявку водителю"

        # send websocket message to front

    except Exception as e:
        return f"Обнаружена ошибка. {e}"
