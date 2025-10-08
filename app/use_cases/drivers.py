from ..infrastructure.db import db_drivers, db_applications
from ..infrastructure.data_schemas import JWTPayload, RoleEnum


from typing import Tuple, Any, Optional

def retrieve_all(causer: JWTPayload) -> Tuple[list[dict[Any, Any]], Optional[str]]:
    try:
        if not causer.login in [RoleEnum.LOGIST, RoleEnum.ADMIN]:
            return [], f"Нет прав"

        res = db_drivers.retrieve_all()
        return res, None
    except Exception as e:
        return [], f"Обнаружена ошибка {e}"


def accept_application(causer: JWTPayload) -> Optional[str]:

    if not causer.login in [RoleEnum.DRIVER]:
        return f"Нет прав"

    try:
        if not db_applications.can_accept(causer.login):
            return "Не получилось принять заявку"

        if not db_applications.accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"


def reject_application(causer: JWTPayload) -> Optional[str]:

    if not causer.login in [RoleEnum.DRIVER]:
        return f"Нет прав"

    try:
        if not db_applications.can_reject(causer.login):
            return "Не получилось принять заявку"

        if not db_applications.accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"



def start_work_shift(causer: JWTPayload) -> Optional[str]:
    try:

        if not causer.login in [RoleEnum.DRIVER]:
            return f"Нет прав"

        success_operation = db_drivers.start_work_shift(causer.login)
        if not success_operation:
            return "Не удалось начать смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"



def stop_work_shift(causer: JWTPayload) -> Optional[str]:
    try:

        if not causer.login in [RoleEnum.DRIVER]:
            return f"Нет прав"

        success_operation = db_drivers.stop_work_shift(causer.login)
        if not success_operation:
            return "Не удалось закончить смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"
