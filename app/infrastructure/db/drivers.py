from psycopg import cursor
from .pool import pool, CONSTRAINT_MESSAGES

from typing import Optional


def start_driver_work_shift(login: str) -> bool:

    '''
    Return true, if succes start work shift
    Return False, if bad
    '''

    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    "UPDATE DRIVERS SET at_work = TRUE WHERE user_login = %(login)s",
                    {"login": login},
                )

                updated = cur.rowcount

                cur.execute(
                        """

                        insert into DRIVER_WORK_SHIFTS (driver_login, start_time, end_time)
                        values (%(login)s, NOW(), NULL);

                        """,
                    {"login": login}
                )


                inserted = cur.rowcount

                success = updated > 0 and inserted > 0
                if success:
                    con.commit()
                    return True

                return False

        except Exception:
            con.rollback()
            return False


def end_driver_work_shift(login: str) -> bool:

    '''
    Return true, if succes stop work shift
    Return False, if bad
    '''

    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    "UPDATE DRIVERS SET at_work = FALSE WHERE login = %(login)s",
                    {"login": login},
                )

                updated = cur.rowcount

                cur.execute(
                        """

                        UPDATE DRIVER_WORK_SHIFTS
                        SET end_time = NOW()
                        WHERE driver_login = %(login)s
                        AND end_time IS NULL;

                        """,
                    {"login": login}
                )


                updated_2 = cur.rowcount

                success = updated > 0 and updated_2 > 0
                if success:
                    con.commit()
                    return True

                return False

        except Exception:
            con.rollback()
            return False


def get_driver(login: str) -> Optional[dict]:

    '''
    Return None if dont find hash
    Return user_json if success
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select * from drivers, users where drivers.user_login = users.login and users.login = %(login)s)",
                        {"login": login},
                        )

            if cur.description:
                colnames = cur.description
                data = cur.fetchone()
                if data is None:
                    return None

                rows = dict(zip(colnames, data))
                return rows

            return None

def driver_at_work(driver_login: str) -> bool:
    '''
    Return True, if at_work true
    Return false else
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select 1 from drivers where user_login = %(login)s and at_work = TRUE LIMIT 1",
                        {"login": driver_login},
                        )
    

            data = cur.fetchone()
            return data != None


