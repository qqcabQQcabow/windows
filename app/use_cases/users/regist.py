from ...infrastructure.db.users import get_user, add_driver, add_logist

from ...infrastructure.auth_utils import create_jwt_token

from ...api_schemas.user_driver_regist_schema import DriverRegistrInfo
from ...api_schemas.user_logist_registr_schema import LogistRegistrInfo

import bcrypt

from typing import Tuple, Optional


def execute_registr_driver(data: DriverRegistrInfo) -> Optional[str]:
    '''
        Return None is success regist
        Return str with denied reson if bad

    '''
    try:
        user = get_user(data.login)
        if user is not None:
            return "Пользователь уже зарегистрирован"

        # может быть, нужно ещё проверить каждое поле? 
        # хотя в бд стоит ограничение

        salt_p = bcrypt.gensalt()
        hash_p = bcrypt.hashpw(data.password.encode('utf-8'), salt_p)

        add_driver(data, hash_p.decode('utf-8'), salt_p.decode('utf-8'))

        return None

    except Exception as exc:
        return f"Обнаружена ошибка. {exc}"

def execute_registr_logits(data: LogistRegistrInfo) -> Optional[str]:
    '''
        Return None is success regist
        Return str with denied reson if bad

    '''
    try:
        user = get_user(data.login)
        if user is not None:
            return "Пользователь уже зарегистрирован"

        # может быть, нужно ещё проверить каждое поле? 
        # хотя в бд стоит ограничение

        salt_p = bcrypt.gensalt()
        hash_p = bcrypt.hashpw(data.password.encode('utf-8'), salt_p)

        add_logist(data, hash_p.decode('utf-8'), salt_p.decode('utf-8'))

        return None

    except Exception as exc:
        return f"Обнаружена ошибка. {exc}"
