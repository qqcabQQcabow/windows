from .pool import pool, CONSTRAINT_MESSAGES
import psycopg

from typing import Optional, Any
from ..data_schemas import TrackForm

def retrieve_work_shifts_history(driver_login: str) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                        """

                        SELECT
                            ws.driver_login,
                            ws.start_time,
                            ws.end_time,
                            t.grz,
                            t.brand,
                            t.color,
                            t.model
                        FROM
                            DRIVER_WORK_SHIFTS ws
                        JOIN
                            TRACKS t
                            ON ws.track_grz = t.grz
                        WHERE
                            ws.driver_login = %(login)s
                        ORDER BY
                            ws.start_time;

                        """,
                        {"login": driver_login}
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []



def retrieve_all() -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                        """

                        SELECT
                            d.user_login,
                            d.raiting,
                            d.at_work,
                            d.passport_numbers,
                            d.driver_license_numbers,
                            d.job_license_numbers,
                            d.snils_number,
                            u.phone,
                            u.email,
                            u.name,
                            u.surname,
                            u.patronymic,
                            u.role,
                            u.born_date
                        FROM drivers AS d
                        JOIN users  AS u ON u.login = d.user_login
                        ORDER BY u.surname, u.name;

                        """
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []

def start_work_shift(driver_login: str, track_grz: str) -> bool:

    '''
    Return true, if succes start work shift
    Return False, if bad
    '''

    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                        """

                        insert into DRIVER_WORK_SHIFTS (driver_login, track_grz, start_time, end_time)
                        values (%(login)s, %(track_grz)s, NOW(), NULL);

                        """,
                    {
                        "login": driver_login,
                        "track_grz": track_grz,
                    }
                )


                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False

        except Exception:
            con.rollback()
            return False

def stop_work_shift(login: str) -> bool:

    '''
    Return true, if succes stop work shift
    Return False, if bad
    '''

    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                        """

                        UPDATE DRIVER_WORK_SHIFTS
                        SET end_time = NOW()
                        WHERE driver_login = %(login)s
                        AND end_time IS NULL;

                        """,
                    {"login": login}
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False

        except Exception:
            con.rollback()
            return False

def get(login: str) -> Optional[dict]:

    '''
    Return None if dont find hash
    Return user_json if success
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select 1 from drivers, users where drivers.user_login = users.login and users.login = %(login)s)",
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


def at_work(driver_login: str) -> bool:
    '''
    Return True, if exist work shift without end_time
    Return false else
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("select 1 from driver_work_shifts where driver_login = %(login)s and end_time is NULL LIMIT 1",
                        {"login": driver_login},
                        )
    

            data = cur.fetchone()
            return data != None


def track_exist(driver_login: str, track_grz: str) -> bool:
    '''
    Return True, if exist work shift without end_time
    Return false else
    '''

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("""

                        SELECT 1 from tracks
                        WHERE driver_login = %(login)s and GRZ = %(track_grz)s
                        LIMIT 1

                        """,
                        {
                            "login": driver_login,
                            "track_grz": track_grz
                        },
                        )
    

            data = cur.fetchone()
            return data != None



def add_track(driver_login: str, track: TrackForm) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        INSERT INTO tracks (driver_login, GRZ, brand, color, model)
                        VALUES (%(driver_login)s, %(grz)s, %(brand)s, %(color)s, %(model)s)
                        RETURNING GRZ

                    """,

                    {
                    "driver_login": driver_login,
                    "grz": track.grz,
                    "brand": track.brand,
                    "color": track.color,
                    "model": track.model
                })
                inserted_grz = cur.fetchone()
                if inserted_grz is None:
                    con.rollback()
                    return False


                con.commit()

                return True

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise

        except Exception as e:
            con.rollback()
            raise e

def del_track(driver_login: str, track_grz: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """
                        delete from tracks where driver_login=%(driver_login)s and GRZ = %(grz)s

                    """,

                    {
                    "driver_login": driver_login,
                    "grz": track_grz,
                })

                if not(cur.rowcount > 0):
                    con.rollback()
                    return False


                con.commit()

                return True

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise

        except Exception as e:
            con.rollback()
            raise e
