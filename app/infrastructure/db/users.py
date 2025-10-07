from psycopg import cursor
from .pool import pool, CONSTRAINT_MESSAGES
import psycopg

from typing import Optional, Tuple
from ...api_schemas.user_driver_regist_schema import DriverRegistrInfo
from ...api_schemas.user_logist_registr_schema import LogistRegistrInfo
from ...infrastructure.auth_utils import RoleEnum

def add_logist(data: LogistRegistrInfo, hash_p: str, salt_p: str):

    '''
    Return None if dont find hash
    Return (hash(str), salt(str))
    '''

    user_data = {
        "login": data.login,
        "hash_password": hash_p,
        "hash_salt": salt_p,
        "phone": data.phone,
        "email": data.email,
        "name": data.name,
        "surname": data.surname,
        "patronymic": data.patronymic,
        "role": RoleEnum.LOGIST,
        "born_date": data.born_date
    }

    logist_data = {
        "user_login": data.login,
    }

    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute("""
                    insert into users (login, hash_password, hash_salt, phone, email, name, surname,
                                       patronymic, role, born_date)
                    values (%(login)s, %(hash_password)s, %(hash_salt)s, %(phone)s, %(email)s, 
                            %(name)s, %(surname)s, %(patronymic)s, %(role)s, to_timestamp(%(born_date)s))
                """, user_data)

                cur.execute("""
                insert into logists (user_login)
                values (%(user_login)s)
                """, logist_data)

                con.commit()

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])

            raise

        except Exception as e:
            con.rollback()
            raise e


def add_driver(data: DriverRegistrInfo, hash_p: str, salt_p: str):

    '''
    Return None if dont find hash
    Return (hash(str), salt(str))
    '''

    user_data = {
        "login": data.login,
        "hash_password": hash_p,
        "hash_salt": salt_p,
        "phone": data.phone,
        "email": data.email,
        "name": data.name,
        "surname": data.surname,
        "patronymic": data.patronymic,
        "role": RoleEnum.DRIVER,
        "born_date": data.born_date
    }

    driver_data = {
        "user_login": data.login,
        "raiting": 0,
        "at_work": False,
        "passport_numbers": data.passport_numbers,
        "driver_license_numbers": data.driver_license_numbers,
        "job_license_numbers": data.job_license_numbers,
        "snils_number": data.snils_numbers
    }

    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute("""
                    insert into users (login, hash_password, hash_salt, phone, email, name, surname,
                                       patronymic, role, born_date)
                    values (%(login)s, %(hash_password)s, %(hash_salt)s, %(phone)s, %(email)s, 
                            %(name)s, %(surname)s, %(patronymic)s, %(role)s, to_timestamp(%(born_date)s))
                """, user_data)

                cur.execute("""
                    insert into drivers (at_work, user_login, raiting, passport_numbers, driver_license_numbers,
                                         job_license_numbers, snils_number)
                    values (%(at_work)s, %(user_login)s, %(raiting)s, %(passport_numbers)s, %(driver_license_numbers)s,
                            %(job_license_numbers)s, %(snils_number)s)
                """, driver_data)

                con.commit()

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])

            raise

        except Exception as e:
            con.rollback()
            raise e


def get_user(login: str) -> Optional[dict]:

    '''
    Return None if dont find hash
    Return user_json if success
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select * from users where login = %(login)s ",
                        {"login": login},
                        )

            if cur.description:
                    # получаем названия колонок
                colnames = cur.description
                # превращаем строки в словари
                data = cur.fetchone()
                if data is None:
                    return None

                rows = dict(zip(colnames, data))
                return rows

            return None


def get_role(login: str) -> Optional[str]:

    '''
    Return None if dont find hash
    Return (hash(str), salt(str))
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select role from users where login = %(login)s ",
                        {"login": login},
                        )

            res = cur.fetchone()
            if res is None:
                return None

            return res[0]


def get_password_hash_and_salt(login: str) -> Optional[Tuple[str, str]]:

    '''
    Return None if dont find hash
    Return (hash(str), salt(str))
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select hash_password, hash_salt from users where login = %(login)s ",
                        {"login": login},
                        )

            hash_p_and_s = cur.fetchone()
            if hash_p_and_s is None:
                return None

            return hash_p_and_s


def change_password_hash(login: str, new_hash: str, new_salt: str) -> bool:

    '''
    Return true, if succes update
    Return False, if changed row count <= 0
    '''


    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    "UPDATE users SET hash_password = %(new_hash)s, hash_salt = %(new_salt)s WHERE login = %(login)s",
                    {"login": login, "new_hash": new_hash, "new_salt": new_salt},
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False

        except Exception:
            con.rollback()
            return False
