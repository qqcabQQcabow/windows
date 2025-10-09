from ..infrastructure.db import db_drivers, db_applications, db_users
from ..infrastructure.data_schemas import JWTPayload, RoleEnum, TrackGrz, TrackForm


from typing import Tuple, Any, Optional


def retrieve_all(causer: JWTPayload) -> Tuple[list[dict[Any, Any]], Optional[str]]:
    try:
        if not causer.role in [RoleEnum.LOGIST, RoleEnum.ADMIN]:
            return [], f"Нет прав"

        res = db_drivers.retrieve_all()
        return res, None
    except Exception as e:
        return [], f"Обнаружена ошибка {e}"


def accept_application(causer: JWTPayload) -> Optional[str]:

    if not causer.role in [RoleEnum.DRIVER]:
        return f"Нет прав"

    try:
        if not db_applications.exist_active_with_driver(causer.login):
            return "Уже есть заявка в работе"

        if not db_applications.can_accept(causer.login):
            return "Не получилось принять заявку"

        if not db_applications.accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"


def reject_application(causer: JWTPayload) -> Optional[str]:

    if not causer.role in [RoleEnum.DRIVER]:
        return f"Нет прав"

    try:
        if not db_applications.can_reject(causer.login):
            return "Не получилось принять заявку"

        if not db_applications.accept_by_driver(causer.login):
            return "Не получилось принять заявку"

        return None

    except Exception as e:
        return f"Обнаружена ошибка. {e}"


def start_work_shift(causer: JWTPayload, data: TrackGrz) -> Optional[str]:
    try:
        if not causer.role in [RoleEnum.DRIVER]:
            return f"Нет прав"

        if db_drivers.at_work(causer.login):
            return f"Смена уже начата"

        if not db_drivers.track_exist(causer.login, data.grz):
            return f"Не существует авто для начала смены "

        success_operation = db_drivers.start_work_shift(causer.login, data.grz)
        if not success_operation:
            return "Не удалось начать смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"


def stop_work_shift(causer: JWTPayload) -> Optional[str]:
    try:
        if not causer.role in [RoleEnum.DRIVER]:
            return f"Нет прав"

        if not db_drivers.at_work(causer.login):
            return f"Смена не начата"

        success_operation = db_drivers.stop_work_shift(causer.login)
        if not success_operation:
            return "Не удалось закончить смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"


def add_track(causer: JWTPayload, data: TrackForm) -> Optional[str]:
    try:
        if not causer.role in [RoleEnum.DRIVER]:
            return f"Нет прав"

        if db_drivers.track_exist(causer.login, data.grz):
            return "Такое авто уже существует"

        db_drivers.add_track(causer.login, data)

        return None

    except Exception as e:
        return f"Ошбика. {e}"


def del_track(causer: JWTPayload, data: TrackGrz) -> Optional[str]:
    try:
        if not causer.role in [RoleEnum.DRIVER]:
            return f"Нет прав"

        if not db_drivers.track_exist(causer.login, data.grz):
            return "Такого авто не существует"

        db_drivers.del_track(causer.login, data.grz)

        return None

    except Exception as e:
        return f"Ошбика. {e}"


def profile(causer: JWTPayload) -> Tuple[dict[Any, Any], Optional[str]]:
    try:
        if not causer.role in [RoleEnum.DRIVER]:
            return {}, "Нет прав"
        return db_users.driver_profile(causer.login), None
    except Exception as e:
        return {}, f"Ошибка. {e}"
