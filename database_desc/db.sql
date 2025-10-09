\c postgres

DROP DATABASE IF EXISTS logist;

CREATE DATABASE logist
WITH
OWNER = postgres
ENCODING = 'UTF8'
LC_COLLATE = 'ru_RU.UTF-8'
LC_CTYPE = 'ru_RU.UTF-8'
TEMPLATE = template0
TABLESPACE = pg_default
CONNECTION LIMIT = -1;

\c logist
DROP TABLE IF EXISTS USERS CASCADE;
DROP TABLE IF EXISTS LOGISTS CASCADE;
DROP TABLE IF EXISTS DRIVERS CASCADE;
DROP TABLE IF EXISTS TRACKS CASCADE;
DROP TABLE IF EXISTS APPLICATIONS CASCADE;
DROP TABLE IF EXISTS APPLICATION_STATES CASCADE;
DROP TABLE IF EXISTS CHAT_MESSAGES CASCADE;

DROP TYPE IF EXISTS user_role_enum;
DROP TYPE IF EXISTS container_type_enum;
DROP TYPE IF EXISTS application_state_enum;


CREATE TYPE user_role_enum AS ENUM ('LOGIST', 'DRIVER', 'ADMIN');

CREATE TABLE USERS (
    avatar VARCHAR(256),

    login VARCHAR(128) PRIMARY KEY NOT NULL,
    hash_password VARCHAR(2048) NOT NULL,
    hash_salt VARCHAR(2048) NOT NULL,
    phone VARCHAR(32) NOT NULL,

    email VARCHAR(256) NOT NULL,
    CONSTRAINT proper_email CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),

    name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    patronymic VARCHAR(64) NOT NULL,

    role user_role_enum NOT NULL,

    born_date TIMESTAMP NOT NULL
);



CREATE TABLE LOGISTS (
    user_login VARCHAR(128) PRIMARY KEY NULL,
    FOREIGN KEY (user_login) REFERENCES USERS(login)
);



CREATE TABLE DRIVERS (
    rating REAL NOT NULL,
    count_rating INT NOT NULL,

    passport_numbers VARCHAR(11) NOT NULL,
    CONSTRAINT passport_rf_format CHECK (passport_numbers ~ '^\d{4} \d{6}$'),

    driver_license_numbers VARCHAR(11) NOT NULL,
    CONSTRAINT vu_rf_format CHECK (driver_license_numbers ~ '^\d{4} \d{6}$'),

    job_license_numbers VARCHAR(7) NOT NULL,
    CONSTRAINT job_license_numbers_check CHECK (job_license_numbers ~ '^\d{7}$'),

    snils_number VARCHAR(14) NOT NULL,
    CONSTRAINT snils_format CHECK (snils_number ~ '^\d{3}-\d{3}-\d{3}-\d{2}$'),

    user_login TEXT PRIMARY KEY NOT NULL,
    FOREIGN KEY (user_login) REFERENCES USERS(login)
);


CREATE TABLE TRACKS (
    GRZ VARCHAR(16) PRIMARY KEY,
    brand VARCHAR(64) NOT NULL,
    color VARCHAR(16) NOT NULL,
    model VARCHAR(64) NOT NULL,

    driver_login VARCHAR(128) NOT NULL,
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login)
);

CREATE TABLE DRIVER_WORK_SHIFTS
(
    driver_login VARCHAR(128) NOT NULL,
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login),

    track_grz VARCHAR(16) NOT NULL,
    FOREIGN KEY (track_grz) REFERENCES TRACKS(GRZ),

    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP
);




CREATE TYPE container_type_enum AS ENUM ('SMALL', 'MEDIUM', 'LARGE');

CREATE TABLE APPLICATIONS (
    id SERIAL PRIMARY KEY,
    
    -- связи
    driver_login VARCHAR(128),
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login),

    logist_login VARCHAR(128) NOT NULL,
    FOREIGN KEY (logist_login) REFERENCES LOGISTS(user_login),

    -- Ожидание приёма заявки
    awaiting_driver_login VARCHAR(128) UNIQUE,
    awaiting_until TIMESTAMP,
    
    -- даты
    created_time TIMESTAMP NOT NULL,
    accepted_time TIMESTAMP,
    
    -- контейнер
    container_type container_type_enum NOT NULL,
    container_count INT NOT NULL,
    container_submission_time TIMESTAMP NOT NULL,
    
    -- погрузка
    container_loading_address VARCHAR(2048) NOT NULL,
    loading_contact VARCHAR(2048) NOT NULL,
    
    -- грузоотправитель
    shipper_name VARCHAR(2048) NOT NULL,
    shipper_address VARCHAR(2048) NOT NULL,
    
    -- груз
    cargo_name VARCHAR(2048) NOT NULL,
    cargo_package_count VARCHAR(2048) NOT NULL,
    cargo_weight VARCHAR(2048) NOT NULL,
    
    -- станции
    departure_station_name VARCHAR(2048) NOT NULL,
    destination_station_name VARCHAR(2048) NOT NULL,
    
    -- грузополучатель
    consignee_name VARCHAR(2048) NOT NULL,
    consignee_address VARCHAR(2048) NOT NULL,
    unloading_contact VARCHAR(2048) NOT NULL,
    
    -- доп
    notes VARCHAR(4096)
);

CREATE TYPE application_state_enum AS ENUM (
    'TERMINAL',             -- Этап №2. Терминал
    'WAREHOUSE',            -- Этап №3. Склад
    'DEPARTURE_STATION',    -- Этап №4. Станция отправления
    'DESTINATION_STATION',  -- Этап №5. Станция назначения
    'CARGO_DELIVERY',       -- Этап №6. Выдача груза
    'EMPTY_CONTAINER_RETURN' -- Этап №7. Сдача порожнего контейнера
);


CREATE TABLE APPLICATION_STATES (
    application_id INT NOT NULL,
    state_name application_state_enum NOT NULL,

    -- driver_login VARCHAR(128),
    -- FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login),

    photos VARCHAR(256),
    document_photos VARCHAR(256),
    time_in TIMESTAMP NOT NULL,
    time_out TIMESTAMP,

    PRIMARY KEY (application_id, state_name),
    FOREIGN KEY (application_id) REFERENCES APPLICATIONS(id)
);


CREATE TABLE CHAT_MESSAGES (

    id SERIAL PRIMARY KEY,

    driver_login VARCHAR(128),
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login),

    logist_login VARCHAR(128) NOT NULL,
    FOREIGN KEY (logist_login) REFERENCES LOGISTS(user_login),


    send_time TIMESTAMP NOT NULL,

    message TEXT NOT NULL
);

insert into users(avatar, login, hash_password, hash_salt, phone, email, name, surname, patronymic, role, born_date)
values
(    NULL,
    'logist1',
    '$2b$12$LuXVue2l7teoBey8qCgxyebAw7svfGQNs8m6j41mDpxJ7sCzJbfky',
    '$2b$12$LuXVue2l7teoBey8qCgxye',
    '78988764454',
    'ann.alx@mail.ru',
    'Анна',
    'Пригожина',
    'Александровка',
    'LOGIST',
    '1994-10-09 00:00:00'),

(    NULL,
    'driver1',
    '$2b$12$FHOoTxM.41bfSCEG4YlWYemAhswHG1tnQNUqj5rfXq5h1aY2jBUde',
    '$2b$12$FHOoTxM.41bfSCEG4YlWYe',
    '79896789909',
    'petr.petr@mail.ru',
    'Петр',
    'Вуйчич',
    'Макарович',
    'DRIVER',
    '1984-10-09 00:00:00')
;

insert into drivers(rating,count_rating, passport_numbers, driver_license_numbers, job_license_numbers, snils_number, user_login)
values
(    0,
     0,
    '6767 898887',
    '4323 098966',
    '6783452',
    '897-232-123-33',
    'driver1')
;

insert into tracks(grz, brand, color, model, driver_login)
values
(    'A000AA00',
    'Pejout',
    'Белый',
    'box',
    'driver1')
;

insert into logists(user_login)
values
(    'logist1')
;
