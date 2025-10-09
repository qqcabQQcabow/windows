from pydantic import NonNegativeFloat
from .pool import pool, CONSTRAINT_MESSAGES
import psycopg
from ..data_schemas import Application, ApplicationState, JWTPayload, RoleEnum
from ..log_utils import logger

from typing import Optional, Any

import logging


def retrieve_all(causer: JWTPayload) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    f"""
                            
                            SELECT * FROM applications where {"logist_login" if causer.role == RoleEnum.LOGIST else "driver_login"} = %(login)s

                            """,
                    {
                        "login": causer.login,
                    },
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []


def retrieve_all_new_for_logist(login: str) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    "SELECT * FROM applications where logist_login = %(login)s and accepted_time is NULL",
                    {"login": login},
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []


def retrieve_all_in_process(causer: JWTPayload) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    f"""
                            
                            select * from applications as ap
                            where (

                                select count(*)<( select count(*) from unnest(enum_range(NULL::application_state_enum)) )
                                from application_states
                                where application_id = ap.id and time_out is not NULL

                                ) = TRUE
                            and accepted_time is not NULL
                            and {"logist_login" if causer.role == RoleEnum.LOGIST else "driver_login"} = %(login)s

                            """,
                    {"login": causer.login},
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []


def retrieve_all_completed(causer: JWTPayload) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    f"""
                            
                            select * from applications as ap
                            where (

                                select count(*)=( select count(*) from unnest(enum_range(NULL::application_state_enum)) )
                                from application_states
                                where application_id = ap.id and time_out is not NULL

                                ) = TRUE
                            and {"logist_login" if causer.role == RoleEnum.LOGIST else "driver_login"} = %(login)s
                            """,
                    {"login": causer.login},
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []

def retrieve_awaiting_by_driver(driver_login: str) -> dict[Any, Any]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    f"""
                            
                            select * from applications as ap
                            WHERE ap.awaiting_driver_login = %(login)s
                            and ap.awaiting_until > NOW()

                            """,
                    {"login": driver_login},
                )

                res = cur.fetchone()
                if res is None:
                    return {}

                desc = cur.description
                if desc is None:
                    return {}

                colnames = [desc[0] for desc in desc]
                return dict(zip(colnames, res))


        except Exception:
            return {}


def create(logist_login: str, data: Application) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO applications (
                        driver_login, logist_login, created_time, container_submission_time,
                        container_type, container_count, container_loading_address, loading_contact,
                        shipper_name, shipper_address, cargo_name, cargo_package_count, cargo_weight,
                        departure_station_name, destination_station_name, consignee_name, consignee_address,
                        unloading_contact, notes
                    ) VALUES (
                        %(driver_login)s, %(logist_login)s, NOW(), 
                        to_timestamp(%(container_submission_time)s),
                        %(container_type)s, %(container_count)s, %(container_loading_address)s, %(loading_contact)s,
                        %(shipper_name)s, %(shipper_address)s, %(cargo_name)s, %(cargo_package_count)s, %(cargo_weight)s,
                        %(departure_station_name)s, %(destination_station_name)s, %(consignee_name)s, %(consignee_address)s,
                        %(unloading_contact)s, %(notes)s
                    ) RETURNING id

                    """,
                    {
                        "driver_login": None,
                        "logist_login": logist_login,
                        "container_submission_time": data.container_submission_time,
                        "container_type": data.container_type.value,
                        "container_count": data.container_count,
                        "container_loading_address": data.container_loading_address,
                        "loading_contact": f"{data.loading_contact_full_name}, {data.loading_contact_phone}",
                        "shipper_name": data.shipper_name,
                        "shipper_address": data.shipper_address,
                        "cargo_name": data.cargo_name,
                        "cargo_package_count": data.cargo_package_count,
                        "cargo_weight": data.cargo_weight,
                        "departure_station_name": data.departure_station_name,
                        "destination_station_name": data.destination_station_name,
                        "consignee_name": data.consignee_name,
                        "consignee_address": data.consignee_address,
                        "unloading_contact": f"{data.unloading_contact_full_name}, {data.unloading_contact_phone}",
                        "notes": data.notes,
                    },
                )

                result = cur.fetchone()
                if result is None:
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


def delete(logist_login: str, id: int) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    """

                        delete from applications where logist_login = %(logist_login)s and application_id = %(id)s

                        """,
                    {"logist_login": logist_login, "id": id},
                )

                deleted_applications = cur.rowcount

                cur.execute(
                    """

                        delete from application_states where application_id = %(id)s

                        """,
                    {"id": id},
                )

                deleted_states = cur.rowcount

                if not (deleted_states > 0 and deleted_applications > 0):
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


def awaiter_info(application_id: int) -> Optional[dict[str, str]]:
    """
    Return current info about wait driver
    If cant found state return None
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        SELECT awaiting_driver_login, awaiting_until
                        FROM applications
                        WHERE s.application_id = %(application_id)s ;

                        """,
                    {"application_id": application_id},
                )

                state = cur.fetchone()
                if state is None:
                    return None

                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    return dict(zip(colnames, state))
        except Exception:
            return None
    return None


def start_await(application_id: int, driver_login: str) -> bool:
    """
    Return True if succes.
    Return False if bad
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        UPDATE applications

                        SET awaiting_driver_login = %(driver_login)s,
                            awaiting_until = NOW() + interval '5 minutes'

                        WHERE id = %(application_id)s ;

                        """,
                    {"application_id": application_id, "driver_login": driver_login},
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False
        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def current_state(application_id: int) -> Optional[dict[str, str]]:
    """
    Return current state
    If cant found state return None
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        SELECT s.*
                        FROM application_states s
                        WHERE s.application_id = %(application_id)s
                        ORDER BY s.time_in DESC
                        LIMIT 1;

                        """,
                    {"application_id": application_id},
                )

                state = cur.fetchone()
                if state is None:
                    return None

                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    return dict(zip(colnames, state))

                return None

        except Exception:
            return None


def can_init_state(state: ApplicationState) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        SELECT
                            cardinality(
                                enum_range(
                                    (
                                        SELECT state_name
                                        FROM application_states
                                        WHERE application_id = %(app_id)s and time_out is not NULL
                                        ORDER BY state_name DESC
                                        LIMIT 1
                                    )::application_state_enum,
                                    %(state_name)s::application_state_enum
                                )
                            ) = 2 AS can_transition;

                        """,
                    {"app_id": state.application_id, "state_name": state.state_name},
                )

                result = cur.fetchone()
                if result is None or result[0] is None:
                    return False

                return result[0]

        except:
            return False


def init_state(state: ApplicationState) -> bool:
    """
    Return True if succes.
    Return False if bad
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        insert into application_states(application_id, state_name, time_in)
                        values(%(application_id)s, %(state_name)s, NOW() )

                        """,
                    {
                        "application_id": state.application_id,
                        "state_name": state.state_name,
                    },
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False
        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def out_state(state: ApplicationState) -> bool:
    """
    Return True if succes.
    Return False if bad
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        UPDATE application_states

                        SET time_out = NOW()

                        WHERE application_id = %(application_id)s
                        and state_name = %(state_name)s
                        and time_out is NULL

                        """,
                    {
                        "application_id": state.application_id,
                        "state_name": state.state_name,
                    },
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False
        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def exist_with_await_driver(driver_login: str) -> bool:
    """
    Return True, if exist with driver_login
    Return false else
    """

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute(
                "select 1 from applications where awaiting_driver_login = %(login)s and awaiting_until > NOW() LIMIT 1",
                {"login": driver_login},
            )

            data = cur.fetchone()
            return data != None


def exist_active_with_driver(driver_login: str) -> bool:
    """
    Return True, if exist with driver_login
    Return false else
    """

    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute(
                """
                        select 1 from applications as ap
                        where ap.driver_login = %(login)s
                            and (

                                select count(*)=( select count(*) from unnest(enum_range(NULL::application_state_enum)) )
                                from application_states
                                where application_id = ap.id and time_out is not NULL

                                ) = FALSE

                        """,
                {"login": driver_login},
            )

            data = cur.fetchone()
            logger.info(data)
            return data != None


def reject_by_driver(driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        UPDATE applications

                        SET awaiting_driver_login = NULL, awaiting_until = NULL

                        WHERE awaiting_driver_login = %(login)s

                        """,
                    {"login": driver_login},
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False
        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def accept_by_driver(driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        UPDATE applications

                        SET driver_login = %(login)s, accepted_time = NOW(), awaiting_driver_login = NULL, awaiting_until = NULL

                        WHERE awaiting_driver_login = %(login)s

                        RETURNING id

                        """,
                    {"login": driver_login},
                )

                id = cur.fetchone()
                if id is None:
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


def can_accept(driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        select 1 from applications 

                        WHERE awaiting_driver_login = %(login)s
                        and awaiting_until > NOW()

                        LIMIT 1


                        """,
                    {"login": driver_login},
                )

                return cur.rowcount > 0

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def can_reject(driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        select 1 from applications 

                        WHERE awaiting_driver_login = %(login)s
                        and awaiting_until > NOW()

                        LIMIT 1


                        """,
                    {"login": driver_login},
                )

                return cur.rowcount > 0

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def change_driver(application_id: int, new_driver_login: str) -> bool:
    """
    Return True if succes.
    Return False if bad
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        UPDATE applications

                        SET driver_login = %(new_driver_login)s,
                            awaiting_until = NULL,
                            awaiting_driver_login = NULL

                        WHERE id = %(application_id)s

                        """,
                    {
                        "application_id": application_id,
                        "new_driver_login": new_driver_login,
                    },
                )

                success = cur.rowcount > 0
                if success:
                    con.commit()
                    return True

                return False
        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def retrieve_all_states(application_id: int) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    """
                            SELECT
                                das.state_name,
                                das.photos,
                                das.document_photos,
                                das.time_in,
                                das.time_out
                            FROM application_states as das
                            WHERE das.application_id = %(application_id)s
                        """,
                    {"application_id": application_id},
                )
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                    return rows
        except Exception:
            return []
    return []


def contains_driver(application_id: int, driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        select 1 from applications 

                        WHERE driver_login = %(login)s
                        and id = %(application_id)s

                        LIMIT 1


                        """,
                    {"login": driver_login, "application_id": application_id},
                )

                return cur.rowcount > 0

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def contains_logist(application_id: int, logist_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:

                cur.execute(
                    """

                        select 1 from applications 

                        WHERE logist_login = %(login)s
                        and id = %(application_id)s

                        LIMIT 1


                        """,
                    {"login": logist_login, "application_id": application_id},
                )

                return cur.rowcount > 0

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])
            raise
        except Exception as e:
            con.rollback()
            raise e


def active_with_driver(driver_login: str) -> bool:
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                cur.execute(
                    """
                            
                            select 1 from applications as ap
                            where (

                                select count(*)<( select count(*) from unnest(enum_range(NULL::application_state_enum)) )
                                from application_states
                                where application_id = ap.id and time_out is not NULL

                                ) = TRUE
                            and driver_login = %(login)s

                            limit 1

                            """,
                    {"login": driver_login},
                )

                result = cur.fetchone()
                logger.info(result)

                if result is None or result[0] is None:
                    return False

                return result[0]

        except Exception as e:
            logger.info(e)
            return False
