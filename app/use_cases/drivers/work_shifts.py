from ...infrastructure.auth_utils import JWTPayload
from typing import Optional

from ...infrastructure.db.drivers import start_driver_work_shift
from ...infrastructure.db.drivers import end_driver_work_shift

def start_driver_work_shift_use_case(causer: JWTPayload) -> Optional[str]:
    try:

        if causer.role != 'DRIVER':
            return "Только водитель может начать смену"

        success_operation = start_driver_work_shift(causer.login)
        if not success_operation:
            return "Не удалось начать смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"



def end_driver_work_shift_use_case(causer: JWTPayload) -> Optional[str]:
    try:

        if causer.role != 'DRIVER':
            return "Только водитель может закончить смену"

        success_operation = end_driver_work_shift(causer.login)
        if not success_operation:
            return "Не удалось закончить смену"

        return None

    except Exception as e:
        return f"Ошбика. {e}"
