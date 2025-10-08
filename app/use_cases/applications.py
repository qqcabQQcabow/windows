from typing import Optional, Tuple, Any

from ..infrastructure.db import db_applications
from ..infrastructure.data_schemas import(
        JWTPayload,
        RoleEnum,
        Application,
        ChangeApplicationDriver,
        ApplicationState,
        )

def create(causer: JWTPayload, data: Application) -> Optional[str]:
    '''
    Return None if success
    Return Err reason, if bad
    '''
    try:
        if causer.role != "LOGIST":
            return "Нет прав"

        success = db_applications.create(causer.login, data)
        if not success:
            return "Не удалось создать заявку"

        return None

    except Exception as e:
        return f"Ошибка. {e}"

def delete(causer: JWTPayload, id: int) -> Optional[str]:
    '''
    Return None if success
    Return Err reason, if bad
    '''
    try:
        if causer.role != "LOGIST":
            return "Нет прав"

        success = db_applications.delete(causer.login, id)
        if not success:
            return "Не удалось удалить заявку"

        return None

    except Exception as e:
        return f"Ошибка. {e}"


def change_driver(causer: JWTPayload, data: ChangeApplicationDriver) -> Optional[str]:
    try:
        if causer.role != RoleEnum.LOGIST:
            return f"Только логист может изменить водителя у заявки"

        success = db_applications.change_driver(data.application_id, data.new_driver_login)
        if not success:
            return f"Не удалось изменить водителя"

        return None
    except Exception as e:
        return f"Ошибка. {e}"


def retrieve_all_states(causer: JWTPayload, application_id: int) -> Tuple[list[dict[Any, Any]], Optional[str]]:
    try:
        if causer.role == RoleEnum.LOGIST and not db_applications.contains_logist(application_id, causer.login):
            return [], f"Нет доступа"
        if causer.role == RoleEnum.DRIVER and not db_applications.contains_driver(application_id, causer.login):
            return [], f"Нет доступа"

        return db_applications.retrieve_all_states(application_id), None
    except Exception as e:
        return [], f"Ошикбка. {e}"


def init_state(causer: JWTPayload, new_state: ApplicationState) -> Optional[str]:
    try:

        if causer.role != RoleEnum.DRIVER:
            return "Только водитель может изменить состояние заявки"

        success = db_applications.init_state(new_state)
        if not success:
            return "Не удалось изменить состояние заявки"

        return None
    except Exception as e:
        return f"Ошибка. {e}"



def out_state(causer: JWTPayload, new_state: ApplicationState) -> Optional[str]:
    try:

        if causer.role != RoleEnum.DRIVER:
            return "Только водитель может изменить состояние заявки"

        success = db_applications.out_state(new_state)
        if not success:
            return "Не удалось изменить состояние заявки"

        return None
    except Exception as e:
        return f"Ошибка. {e}"
