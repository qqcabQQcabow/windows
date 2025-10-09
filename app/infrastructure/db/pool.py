from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("host")
port = os.getenv("port")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")

CONSTRAINT_MESSAGES = {
    # USERS
    "proper_email": "Неверный формат email",  # CHECK на email
    "users_pkey": "Пользователь с таким логином уже существует",  # PRIMARY KEY на login
    # DRIVERS
    "drivers_user_login_fkey": "Водитель не найден",  # FOREIGN KEY user_login → USERS
    "passport_rf_format": "Неверный формат паспорта РФ",  # CHECK
    "vu_rf_format": "Неверный формат ВУ РФ",  # CHECK
    "job_license_numbers_check": "Неверный формат трудовой книжки",  # CHECK
    "snils_format": "Неверный формат СНИЛС",  # CHECK
    "drivers_pkey": "Водитель с таким логином уже существует",  # PRIMARY KEY user_login
    # LOGISTS
    "logists_user_login_fkey": "Логист не найден",  # FOREIGN KEY user_login → USERS
    "logists_pkey": "Логист с таким логином уже существует",  # PRIMARY KEY user_login
    # TRACKS
    "tracks_driver_login_fkey": "Водитель для автомобиля не найден",  # FOREIGN KEY driver_login → DRIVERS
    "tracks_pkey": "Автомобиль с таким GRZ уже существует",  # PRIMARY KEY GRZ
    # DRIVER_APPLICATIONS
    "applications_driver_login_fkey": "Водитель для заявки не найден",  # FOREIGN KEY driver_login → DRIVERS
    "applications_logist_login_fkey": "Логист для заявки не найден",  # FOREIGN KEY logist_login → LOGISTS
    "applications_pkey": "Заявка с таким id уже существует",  # PRIMARY KEY id
    # DRIVER_APPLICATION_STATES
    "application_states_application_id_fkey": "Заявка для статуса не найдена",  # FOREIGN KEY application_id → DRIVER_APPLICATIONS
    "application_states_pkey": "Статус с таким id уже существует",  # PRIMARY KEY id
}

# some connect settings
pool = ConnectionPool(
    f"host={host} port={port} dbname={dbname} user={user} password={password}"
)
