from .pool import pool, CONSTRAINT_MESSAGES
import psycopg
from ...api_schemas.driver_application_schema import DriverApplication

from typing import Optional, Any

def retrieve_all_for_driver(login: str) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM driver_applications where driver_login = %(login)s", {"login": login})
            if cur.description:
                colnames = [desc[0] for desc in cur.description]
                rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                return rows
    return []




def retrieve_all_for_logist(login: str) -> list[dict[Any, Any]]:
    with pool.connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM driver_applications where logist_login = %(login)s", {"login": login})
            if cur.description:
                colnames = [desc[0] for desc in cur.description]
                rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                return rows
    return []



def create_driver_application(logist_login: str, data: DriverApplication):
    """
    Create driver application and create DA_state APPLICATION.
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                # INSERT в DRIVER_APPLICATIONS
                cur.execute(
                        """
                    INSERT INTO DRIVER_APPLICATIONS (
                        driver_login, logist_login, submission_time, container_submission_time,
                        container_type, container_count, container_loading_address, loading_contact,
                        shipper_name, shipper_address, cargo_name, cargo_package_count, cargo_weight,
                        departure_station_name, destination_station_name, consignee_name, consignee_address,
                        unloading_contact, notes
                    ) VALUES (
                        %(driver_login)s, %(logist_login)s, to_timestamp(%(submission_time)s), 
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
                    "submission_time": data.submission_time,
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
                    "notes": data.notes
                })

                # Получаем ID вставленной заявки
                result = cur.fetchone()
                application_id = 0
                if result is not None:
                    application_id = result[0]

                # INSERT начального статуса в DRIVER_APPLICATION_STATES
                cur.execute("""
                    INSERT INTO DRIVER_APPLICATION_STATES (
                        application_id, state_name, state_date
                    ) VALUES (
                        %(application_id)s, 'APPLICATION', NOW()
                    )
                """, {"application_id": application_id})

                # Коммит транзакции
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

def start_await(application_id: int, driver_login: str):
    """
    """
    with pool.connection() as con:
        try:
            with con.cursor() as cur:
                a = 9

        except psycopg.Error as e:
            con.rollback()
            constraint_name = getattr(e.diag, "constraint_name", None)
            if constraint_name and constraint_name in CONSTRAINT_MESSAGES:
                raise Exception(CONSTRAINT_MESSAGES[constraint_name])

            raise

        except Exception as e:
            con.rollback()
            raise e


def get_current_state(application_id: int) -> Optional[dict]:
    '''
    Return current state
    If cant found state return None
    '''
    with pool.connection() as con:
        with con.cursor() as cur:

            cur.execute(

                    """

                    SELECT s.*
                    FROM DRIVER_APPLICATION_STATES s
                    WHERE s.application_id = %(application_id)s
                    ORDER BY s.state_date DESC
                    LIMIT 1;

                    """,

                    {"application_id": application_id}

                    )

            state = cur.fetchone()
            if state is None:
                return None

            if cur.description:
                colnames = [desc[0] for desc in cur.description]
                return dict(zip(colnames, state))

    return None

def get_all_states(application_id: int) -> list[dict[Any, Any]]:
    '''
    Return current state
    If cant found state return None
    '''
    with pool.connection() as con:
        with con.cursor() as cur:

            cur.execute(

                    """
                    SELECT s.*
                    FROM DRIVER_APPLICATION_STATES s
                    WHERE s.application_id = %(application_id)s
                    ORDER BY s.state_date DESC
                    """,

                    {"application_id": application_id}

                    )

            if cur.description:
                colnames = [desc[0] for desc in cur.description]
                rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
                return rows

    return []
