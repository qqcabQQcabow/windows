from ...infrastructure.auth_utils import JWTPayload, RoleEnum
from ...infrastructure.db.driver_applications import accept_by_driver, can_accept

from typing import Optional


def accept(causer: JWTPayload) -> Optional[str]:

    if causer.role != RoleEnum.DRIVER:
        return f"Нет прав"

    try:
        if not can_accept(causer.login):
            return "Не получилось принять заявку"

        if not accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"


def reject(causer: JWTPayload) -> Optional[str]:

    if causer.role != RoleEnum.DRIVER:
        return f"Нет прав"

    try:
        if not can_accept(causer.login):
            return "Не получилось принять заявку"

        if not accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"
