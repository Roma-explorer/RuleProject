CREATE TABLE Description (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL
);

CREATE TABLE Reason(
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL
);

CREATE TYPE status AS ENUM ('открыта', 'в работе', 'закрыта', 'возобновлена');

CREATE TABLE Mistake(
    id SERIAL PRIMARY KEY,
    reason_id integer REFERENCES Reason(id),
    description_id integer REFERENCES Description(id) NOT NULL,
    status status NOT NULL DEFAULT 'открыта',
    planned_hours integer CHECK (planned_hours > 0),
    date_start DATE,
    date_end DATE,
    CHECK (date_end > date_start)
);

CREATE TABLE Task(
    id SERIAL PRIMARY KEY,
    description_id integer REFERENCES Description(id),
    status status NOT NULL DEFAULT 'открыта',
    planned_hours integer CHECK (planned_hours > 0),
    date_start DATE,
    date_end DATE,
    CHECK (date_end > date_start)
);



CREATE TABLE Feature(
    id SERIAL PRIMARY KEY,
    description_id integer REFERENCES Description(id),
    planned_hours integer CHECK (planned_hours > 0),
    date_start DATE,
    date_end DATE,
    CHECK (date_end > date_start)
);

ALTER TABLE Task ADD COLUMN feature_id INTEGER REFERENCES feature(id);
ALTER TABLE Mistake ADD COLUMN feature_id INTEGER REFERENCES feature(id);
ALTER TABLE Mistake ADD COLUMN task_id INTEGER REFERENCES task(id);

CREATE TABLE Country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(56) NOT NULL
);

CREATE TABLE Region (
    id SERIAL PRIMARY KEY,
    name VARCHAR(85) NOT NULL,
    country_id INTEGER REFERENCES Country(id) NOT NULL
);

CREATE TABLE City (
    id SERIAL PRIMARY KEY,
    name VARCHAR(85) NOT NULL,
    region_id INTEGER REFERENCES Region(id) NOT NULL
);

CREATE TABLE Street (
    id SERIAL PRIMARY KEY,
    name VARCHAR(140) NOT NULL,
    city_id INTEGER REFERENCES City(id) NOT NULL
);

CREATE TABLE Address (
    country_id INTEGER REFERENCES Country(id) NOT NULL,
    region_id INTEGER REFERENCES Region(id) NOT NULL,
    city_id INTEGER REFERENCES City(id) NOT NULL,
    street_id INTEGER REFERENCES Street(id) NOT NULL,
    house_number INTEGER CHECK (house_number > 0)
);

CREATE TABLE Position (
    id SERIAL PRIMARY KEY,
    name VARCHAR(70) NOT NULL
);

CREATE TABLE EmployeeContract (
    id SERIAL PRIMARY KEY,
    position_id INT REFERENCES Position(id) NOT NULL,
    num_hours SMALLINT NOT NULL,
    work_time INTERVAL,
    probation_time DATE,
    work_type VARCHAR(100) NOT NULL,
    sign_date DATE NOT NULL
);

ALTER TABLE address ADD id SERIAL PRIMARY KEY;

CREATE TABLE Department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address_id INT REFERENCES Address(id)
);

CREATE TYPE Sex as ENUM ('Мужской', 'Женский');

CREATE DOMAIN phone_number AS VARCHAR(12) CHECK(VALUE ~ '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$');

CREATE DOMAIN email_address AS citext CHECK (value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$');

CREATE TABLE Employee (
    id SERIAL PRIMARY KEY,
    sex Sex NOT NULL,
    birth_date DATE NOT NULL,
    position_id INT REFERENCES position(id) NOT NULL,
    department_id INT REFERENCES department(id) NOT NULL,
    phone phone_number NOT NULL,
    email email_address NOT NULL
);

ALTER TABLE mistake ADD employee_id INTEGER REFERENCES employee(id) NOT NULL;
ALTER TABLE task ADD employee_id INTEGER REFERENCES employee(id) NOT NULL;
ALTER TABLE employeecontract ADD employee_id INTEGER REFERENCES employee(id) NOT NULL;

CREATE TABLE WorkTimePeriod (
    id SERIAL PRIMARY KEY,
    arrival_time timestamp,
    leave_time timestamp,
    early_leave BOOLEAN,
    late_arrival BOOLEAN
);

CREATE TYPE med_certificate_status AS ENUM ('Открыт', 'Продлён', 'Закрыт');

CREATE TABLE MedicalCertificate(
    id SERIAL PRIMARY KEY,
    doctor_name varchar(150) NOT NULL,
    doctor_surname varchar(150) NOT NULL,
    doctor_lastname varchar(150),
    status med_certificate_status NOT NULL,
    ill_time interval NOT NULL,
    reason VARCHAR(250) NOT NULL,
    hospital_name VARCHAR(250) NOT NULL,
    is_continue BOOLEAN,
    OGRN VARCHAR(13)
);

ALTER TABLE employee ADD COLUMN name varchar(150) NOT NULL;
ALTER TABLE employee ADD COLUMN surname varchar(150) NOT NULL;
ALTER TABLE employee ADD COLUMN lastname varchar(150);
ALTER TABLE MedicalCertificate ADD employee_id INTEGER REFERENCES employee(id);

CREATE TABLE Client(
    id SERIAL PRIMARY KEY,
    account VARCHAR(20),
    inn VARCHAR(12) NOT NULL,
    OGRN VARCHAR(13) NOT NULL,
    phone phone_number NOT NULL,
    email email_address NOT NULL,
    address INTEGER REFERENCES address(id) NOT NULL
);

CREATE TABLE PaymentInvoice(
    id SERIAL PRIMARY KEY,
    date date NOT NULL ,
    account VARCHAR(20) NOT NULL ,
    receive_date date
);

CREATE TABLE TechTask(
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    purpose TEXT,
    control_procedures TEXT,
    work_order TEXT
);

CREATE TABLE Requirement(
    id SERIAL PRIMARY KEY,
    GOST VARCHAR(10),
    content TEXT NOT NULL,
    tech_task_id INTEGER REFERENCES TechTask(id) NOT NULL
);

CREATE TABLE TransferReceiveAct(
    id SERIAL PRIMARY KEY,
    type VARCHAR(100),
    date date NOT NULL,
    functions TEXT,
    client_side TEXT NOT NULL,
    COMPANY_side TEXT NOT NULL
);

CREATE TABLE Contract(
    number INTEGER PRIMARY KEY,
    risks TEXT,
    tasks TEXT,
    cost DECIMAL NOT NULL,
    sign_date date NOT NULL,
    duration VARCHAR(100),
    client_id INTEGER REFERENCES client(id) NOT NULL,
    tech_task_id INTEGER REFERENCES techtask(id),
    account_id INTEGER REFERENCES paymentinvoice(id),
    act_id INTEGER REFERENCES transferreceiveact(id)
);

CREATE TABLE Project (
    id SERIAL,
    name VARCHAR(100) NOT NULL,
    date_start date NOT NULL DEFAULT now(),
    date_end date,
    contract_id INTEGER REFERENCES contract(number)
);

ALTER TABLE Project ADD PRIMARY KEY (id);

CREATE TABLE DepartmentProject(
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES project(id) NOT NULL ,
    department_id INTEGER REFERENCES department(id) NOT NULL
);

ALTER TABLE Project ADD project_id INTEGER REFERENCES DepartmentProject(id) NOT NULL;
ALTER TABLE feature ALTER COLUMN project_id SET NOT NULL;

CREATE TABLE EmployeeProject
(
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES project(id),
    employee_id INTEGER REFERENCES employee(id),
    time_periods interval[]
);

CREATE TABLE EmployeeProjectFeature(
    id SERIAL PRIMARY KEY,
    employeeproj_id INTEGER REFERENCES EmployeeProject(id) NOT NULL,
    feature_id INTEGER REFERENCES feature(id) NOT NULL
);

ALTER TABLE EmployeeProject ADD feature_id INTEGER REFERENCES EmployeeProjectFeature(id);
ALTER TABLE feature ADD employeeproj_id INTEGER REFERENCES EmployeeProjectFeature(id);
ALTER TABLE project RENAME project_id TO department_id;

ALTER TABLE feature DROP COLUMN employeeproj_id;
ALTER TABLE employeeproject DROP feature_id;
ALTER TABLE project DROP COLUMN department_id;

ALTER TABLE employeeprojectfeature ADD CONSTRAINT uni UNIQUE (feature_id, employeeproj_id);
ALTER TABLE departmentproject ADD CONSTRAINT onlyuni UNIQUE (project_id, department_id);

ALTER TABLE client RENAME address TO address_id;
