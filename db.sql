-- 1. First drop existing tables if they exist (to avoid conflicts)

DROP DATABASE IF EXISTS logist;


DROP TABLE IF EXISTS USERS CASCADE;
DROP TABLE IF EXISTS LOGISTS CASCADE;
DROP TABLE IF EXISTS DRIVERS CASCADE;
DROP TABLE IF EXISTS TRACKS CASCADE;
DROP TABLE IF EXISTS DRIVER_APPLICATIONS CASCADE;
DROP TABLE IF EXISTS DRIVER_APPLICATION_STATES CASCADE;

-- 2. Create database with valid locale


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

CREATE TABLE USERS (
    login TEXT PRIMARY KEY NOT NULL,
    hash_password TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    FIO TEXT NOT NULL,
    role TEXT NOT NULL,
    born_date TIMESTAMP NOT NULL
);

CREATE TABLE LOGISTS (
    user_login TEXT PRIMARY KEY NULL,
    FOREIGN KEY (user_login) REFERENCES USERS(login)
);


CREATE TABLE DRIVERS (
    raiting INT NOT NULL,

    personal_data TEXT NOT NULL,

    user_login TEXT PRIMARY KEY NOT NULL,
    FOREIGN KEY (user_login) REFERENCES USERS(login)
);

-- Таблица автомобилей
CREATE TABLE TRACKS (
    GRZ TEXT PRIMARY KEY,
    brand TEXT NOT NULL,
    color TEXT NOT NULL,
    model TEXT NOT NULL,

    driver_login TEXT NOT NULL,
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login)
);

CREATE TYPE container_type_enum AS ENUM ('SMALL', 'MEDIUM', 'LARGE');

CREATE TABLE DRIVER_APPLICATIONS (
    id SERIAL PRIMARY KEY,
    
    -- связи
    driver_login TEXT NOT NULL,
    FOREIGN KEY (driver_login) REFERENCES DRIVERS(user_login),

    logist_login TEXT NOT NULL,
    FOREIGN KEY (logist_login) REFERENCES LOGISTS(user_login),
    
    -- даты
    submission_time TIMESTAMP NOT NULL,
    container_submission_time TIMESTAMP NOT NULL,
    
    -- контейнер
    container_type container_type_enum NOT NULL,
    container_count INT NOT NULL,
    
    -- погрузка
    container_loading_address TEXT NOT NULL,
    loading_contact TEXT NOT NULL,
    
    -- грузоотправитель
    shipper_name TEXT NOT NULL,
    shipper_address TEXT NOT NULL,
    
    -- груз
    cargo_name TEXT NOT NULL,
    cargo_package_count INT NOT NULL,
    cargo_weight INT NOT NULL,
    
    -- станции
    departure_station_name TEXT NOT NULL,
    destination_station_name TEXT NOT NULL,
    
    -- грузополучатель
    consignee_name TEXT NOT NULL,
    consignee_address TEXT NOT NULL,
    unloading_contact TEXT NOT NULL,
    
    -- доп
    notes TEXT
);

CREATE TYPE driver_application_state_enum AS ENUM (
    'APPLICATION',          -- Этап №1. Заявка
    'TERMINAL',             -- Этап №2. Терминал
    'WAREHOUSE',            -- Этап №3. Склад
    'DEPARTURE_STATION',    -- Этап №4. Станция отправления
    'DESTINATION_STATION',  -- Этап №5. Станция назначения
    'CARGO_DELIVERY',       -- Этап №6. Выдача груза
    'EMPTY_CONTAINER_RETURN' -- Этап №7. Сдача порожнего контейнера
);


-- Активные сессии парковки
CREATE TABLE DRIVER_APPLICATION_STATES (
    id SERIAL PRIMARY KEY,
    application_id SERIAL NOT NULL,
    FOREIGN KEY (application_id) REFERENCES DRIVER_APPLICATIONS(id),

    state_name driver_application_state_enum NOT NULL,

    photos TEXT,
    document_photos TEXT,
    state_date TIMESTAMP NOT NULL
);

-- Users
INSERT INTO USERS (login, hash_password, phone, email, fio, role, born_date)
VALUES
('driver1', 'hash1', '1234567890', 'd1@example.com', 'Ivan Ivanov', 'DRIVER', '1990-01-01'),
('logist1', 'hash2', '0987654321', 'l1@example.com', 'Petr Petrov', 'LOGIST', '1985-02-02');

-- Drivers/Logists
INSERT INTO DRIVERS (user_login, raiting, personal_data)
VALUES ('driver1', 5, 'Passport 12345');
INSERT INTO LOGISTS (user_login) VALUES ('logist1');

-- Tracks
INSERT INTO TRACKS (grz, brand, color, model, driver_login)
VALUES ('A123BC', 'Volvo', 'Blue', 'FH16', 'driver1');

-- Applications
INSERT INTO DRIVER_APPLICATIONS (
    driver_login, logist_login, submission_time, container_submission_time,
    container_type, container_count, container_loading_address, loading_contact,
    shipper_name, shipper_address, cargo_name, cargo_package_count, cargo_weight,
    departure_station_name, destination_station_name, consignee_name, consignee_address,
    unloading_contact, notes
) VALUES (
    'driver1', 'logist1', NOW(), NOW() + interval '2 days',
    'MEDIUM', 2, 'Moscow, Lenina 1', 'Ivan Petrov',
    'OOO Roga', 'Moscow, Tverskaya 5', 'Electronics', 10, 5000,
    'Moscow Station', 'SPB Station', 'OOO Horns', 'SPB, Nevsky 10',
    'Sergey Smirnov', 'Urgent delivery'
);

-- States
INSERT INTO DRIVER_APPLICATION_STATES (application_id, state_name, photos, document_photos, state_date)
VALUES
(1, 'APPLICATION', 'photo1.jpg', 'doc1.pdf', NOW()),
(1, 'TERMINAL', 'photo2.jpg', 'doc2.pdf', NOW() + interval '1 day');
