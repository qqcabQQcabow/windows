from typing import Tuple, Optional
import bcrypt

from ..infrastructure import auth_utils
from ..infrastructure.data_schemas import (
    LoginInfo,
    RoleEnum,
    DriverRegistrInfo,
    LogistRegistrInfo,
)
from ..infrastructure.db import db_users


def log_in(data: LoginInfo) -> Tuple[str, Optional[str]]:
    """
    Return [jwt_token(str), None] if success auth
    Return ["", DeniedReason(str)] if problem with auth

    """
    try:
        res = db_users.get_password_hash_and_salt(data.login)
        if res is None:
            return ("", "Не найден пользователь")

        hash_p_source, salt_p = res

        hash_p = bcrypt.hashpw(
            data.password.encode("utf-8"), salt_p.encode("utf-8")
        ).decode("utf-8")

        if hash_p_source != hash_p:
            return ("", "Неверный пароль")

        role = db_users.get_role(data.login)
        if role is None:
            return ("", "Не удалось получить роль")

        token = auth_utils.create_jwt_token(data.login, RoleEnum(role))

        return (token, None)

    except Exception as exc:
        return ("", f"Обнаружена ошибка. {exc}")


def registr_driver(data: DriverRegistrInfo) -> Optional[str]:
    """
    Return None is success regist
    Return str with denied reson if bad

    """
    try:
        user = db_users.get(data.login)
        if user is not None:
            return "Пользователь уже зарегистрирован"

        salt_p = bcrypt.gensalt()
        hash_p = bcrypt.hashpw(data.password.encode("utf-8"), salt_p)

        db_users.add_driver(data, hash_p.decode("utf-8"), salt_p.decode("utf-8"))

        return None

    except Exception as exc:
        return f"Обнаружена ошибка. {exc}"


def registr_logits(data: LogistRegistrInfo) -> Optional[str]:
    """
    Return None is success regist
    Return str with denied reson if bad

    """
    try:
        user = db_users.get(data.login)
        if user is not None:
            return "Пользователь уже зарегистрирован"

        salt_p = bcrypt.gensalt()
        hash_p = bcrypt.hashpw(data.password.encode("utf-8"), salt_p)

        success = db_users.add_logist(
            data, hash_p.decode("utf-8"), salt_p.decode("utf-8")
        )
        if not success:
            return "Не удалось зарегистрировать логиста"

        return None

    except Exception as exc:
        return f"Обнаружена ошибка. {exc}"
