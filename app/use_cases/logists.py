from ..infrastructure.db import db_applications, db_users, db_drivers
from ..infrastructure.data_schemas import (
    JWTPayload,
    SendApplication,
    ApplicationStateEnum,
    RoleEnum,
)

from typing import Optional, Tuple, Any


def send_application_to_driver(
    causer: JWTPayload, data: SendApplication
) -> Optional[str]:
    try:
        if causer.role != "LOGIST":
            return f"Нет прав"

        da_state = db_applications.current_state(data.application_id)
        if da_state is not None:
            return f"Отправить можно только созданную заявку"

        driver = db_users.get(data.driver_login)
        if driver is None:
            return f"Водитель с логином {data.driver_login} не найден"

        if not db_drivers.at_work(data.driver_login):
            return f"Водитель не на работе"

        if db_applications.exist_active_with_driver(data.driver_login):
            return f"Водитель уже имеет заявку в работе"

        if db_applications.exist_with_await_driver(data.driver_login):
            return f"Водитель уже имеет заявку на подтверждение"

        if not db_applications.start_await(data.application_id, data.driver_login):
            return f"Не удалось отправить заявку водителю"

        # TODO
        # send websocket message to front

    except Exception as e:
        return f"Обнаружена ошибка. {e}"


def profile(causer: JWTPayload) -> Tuple[dict[Any, Any], Optional[str]]:
    try:
        if not causer.role in [RoleEnum.LOGIST]:
            return {}, "Нет прав"
        return db_users.logist_profile(causer.login), None
    except Exception as e:
        return {}, f"Ошибка. {e}"
