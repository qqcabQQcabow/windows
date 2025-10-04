from ...infrastructure.db.users import get_password_hash_and_salt, get_role

from ...infrastructure.auth_utils import create_jwt_token

import bcrypt

from typing import Tuple, Optional

from ...api_schemas.user_login_schema import LoginInfo


def execute_log_in(data: LoginInfo) -> Tuple[str, Optional[str]]:
    '''
        Return [jwt_token(str), None] if success auth
        Return ["", DeniedReason(str)] if problem with auth

    '''
    try:
        res = get_password_hash_and_salt(data.login);
        if res is None:
            return ("", "Не найден пользователь")

        hash_p_source, salt_p = res

        hash_p = bcrypt.hashpw(data.password.encode('utf-8'), salt_p.encode('utf-8')).decode('utf-8')

        if hash_p_source != hash_p:
            return ("", "Неверный пароль")

        role = get_role(data.login)
        if role is None:
            return ("", "Не найден пользователь")

        token = create_jwt_token(data.login, role);

        return (token, None)

    except Exception as exc:
        return ("", f"Обнаружена ошибка. {exc}")
