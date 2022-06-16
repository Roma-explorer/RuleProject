# coding: utf-8
import enum
from sqlalchemy import ARRAY, Boolean, CheckConstraint, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, \
    SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, server_default=text("nextval('country_id_seq'::regclass)"))
    name = Column(String(56), nullable=False)

    regions = relationship('Region', back_populates='country')
    addresses = relationship('Address', back_populates='country')


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True, server_default=text("nextval('description_id_seq'::regclass)"))
    text = Column(Text, nullable=False)
    
    mistakes = relationship('Mistake', back_populates='description')
    tasks = relationship('Task', back_populates='description')
    features = relationship('Feature', back_populates='description')


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class PaymentInvoice(Base):
    __tablename__ = 'paymentinvoice'

    id = Column(Integer, primary_key=True, server_default=text("nextval('paymentinvoice_id_seq'::regclass)"))
    date = Column(Date, nullable=False)
    account = Column(String(20), nullable=False)
    receive_date = Column(Date)
    
    contract = relationship('Contract', back_populates='account')


class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True, server_default=text("nextval('position_id_seq'::regclass)"))
    name = Column(String(70), nullable=False)
    
    contracts = relationship('EmployeeContract', back_populates='position')
    employees = relationship('Employee', back_populates='position')


class Reason(Base):
    __tablename__ = 'reason'

    id = Column(Integer, primary_key=True, server_default=text("nextval('reason_id_seq'::regclass)"))
    text = Column(Text, nullable=False)
    mistakes = relationship('Mistake', back_populates='reason')


class SpatialRefSy(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))


class TechTask(Base):
    __tablename__ = 'techtask'

    id = Column(Integer, primary_key=True, server_default=text("nextval('techtask_id_seq'::regclass)"))
    number = Column(String(15), nullable=False)
    description = Column(Text, nullable=False)
    purpose = Column(Text)
    control_procedures = Column(Text)
    work_order = Column(Text)
    
    contract = relationship('Contract', back_populates='tech_task')
    requirements = relationship('Requirement', back_populates='tech_task')


class TransferReceiveAct(Base):
    __tablename__ = 'transferreceiveact'

    id = Column(Integer, primary_key=True, server_default=text("nextval('transferreceiveact_id_seq'::regclass)"))
    type = Column(String(100))
    date = Column(Date, nullable=False)
    functions = Column(Text)
    client_side = Column(Text, nullable=False)
    company_side = Column(Text, nullable=False)
    
    contract = relationship('Contract', back_populates='act')


class WorkTimePeriod(Base):
    __tablename__ = 'worktimeperiod'

    id = Column(Integer, primary_key=True, server_default=text("nextval('worktimeperiod_id_seq'::regclass)"))
    arrival_time = Column(DateTime)
    leave_time = Column(DateTime)
    early_leave = Column(Boolean)
    late_arrival = Column(Boolean)


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, server_default=text("nextval('region_id_seq'::regclass)"))
    name = Column(String(85), nullable=False)
    country_id = Column(ForeignKey('country.id'), nullable=False)

    country = relationship('Country', back_populates='regions')

    cities = relationship('City', back_populates='region')
    addresses = relationship('Address', back_populates='region')


class Requirement(Base):
    __tablename__ = 'requirement'

    id = Column(Integer, primary_key=True, server_default=text("nextval('requirement_id_seq'::regclass)"))
    gost = Column(String(10))
    content = Column(Text, nullable=False)
    tech_task_id = Column(ForeignKey('techtask.id'), nullable=False)

    tech_task = relationship('TechTask', back_populates='requirements')


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, server_default=text("nextval('city_id_seq'::regclass)"))
    name = Column(String(85), nullable=False)
    region_id = Column(ForeignKey('region.id'), nullable=False)

    region = relationship('Region', back_populates='cities')

    streets = relationship('Street', back_populates='city')
    addresses = relationship('Address', back_populates='city')


class Street(Base):
    __tablename__ = 'street'

    id = Column(Integer, primary_key=True, server_default=text("nextval('street_id_seq'::regclass)"))
    name = Column(String(140), nullable=False)
    city_id = Column(ForeignKey('city.id'), nullable=False)

    city = relationship('City', back_populates='streets')

    addresses = relationship('Address', back_populates='street')


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = (
        CheckConstraint('house_number > 0'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('address_id_seq'::regclass)"))
    country_id = Column(ForeignKey('country.id'), nullable=False)
    region_id = Column(ForeignKey('region.id'), nullable=False)
    city_id = Column(ForeignKey('city.id'), nullable=False)
    street_id = Column(ForeignKey('street.id'), nullable=False)
    house_number = Column(Integer)

    city = relationship('City', back_populates='addresses')
    country = relationship('Country', back_populates='addresses')
    region = relationship('Region', back_populates='addresses')
    street = relationship('Street', back_populates='addresses')

    departments = relationship('Department', back_populates='address')
    clients = relationship('Client', back_populates='address')


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, server_default=text("nextval('client_id_seq'::regclass)"))
    name = Column(String(150), nullable=False)
    account = Column(String(20))
    inn = Column(String(12), nullable=False)
    ogrn = Column(String(13), nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address_id = Column(ForeignKey('address.id'), nullable=False)

    address = relationship('Address', back_populates='clients')
    
    contracts = relationship('Contract', back_populates='client')


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, server_default=text("nextval('department_id_seq'::regclass)"))
    name = Column(String(100), nullable=False)
    address_id = Column(ForeignKey('address.id'))

    address = relationship('Address', back_populates='departments')
    
    projects = relationship('DepartmentProject', back_populates='departments')
    employees = relationship('Employee', back_populates='department')


class Contract(Base):
    __tablename__ = 'contract'

    number = Column(Integer, primary_key=True)
    risks = Column(Text)
    tasks = Column(Text)
    cost = Column(Numeric, nullable=False)
    sign_date = Column(Date, nullable=False)
    duration = Column(String(100))
    client_id = Column(ForeignKey('client.id'), nullable=False)
    tech_task_id = Column(ForeignKey('techtask.id'))
    account_id = Column(ForeignKey('paymentinvoice.id'))
    act_id = Column(ForeignKey('transferreceiveact.id'))

    account = relationship('PaymentInvoice', back_populates='contract')
    act = relationship('TransferReceiveAct', back_populates='contract')
    client = relationship('Client', back_populates='contracts')
    tech_task = relationship('TechTask', back_populates='contract')
    
    project = relationship('Project', back_populates='contract')


class Sex(enum.Enum):
    male = 'Мужской'
    female = 'Женский'


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, server_default=text("nextval('employee_id_seq'::regclass)"))
    sex = Column(Enum(Sex, name='sex'), nullable=True)
    birth_date = Column(Date, nullable=False)
    position_id = Column(ForeignKey('position.id'), nullable=False)
    department_id = Column(ForeignKey('department.id'), nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String(150), nullable=False)
    surname = Column(String(150), nullable=False)
    lastname = Column(String(150))

    department = relationship('Department', back_populates='employees')
    position = relationship('Position', back_populates='employees')
    
    mistakes = relationship('Mistake', back_populates='employee')
    tasks = relationship('Task', back_populates='employee')
    projects = relationship('EmployeeProject', back_populates='employees')
    med_certificates = relationship('MedicalCertificate', back_populates='employee')
    contracts = relationship('EmployeeContract', back_populates='employee')
    head_projects = relationship('Project', back_populates='head')
    user = relationship('User', back_populates='employee')


class EmployeeContract(Base):
    __tablename__ = 'employeecontract'

    id = Column(Integer, primary_key=True, server_default=text("nextval('employeecontract_id_seq'::regclass)"))
    position_id = Column(ForeignKey('position.id'), nullable=False)
    num_hours = Column(SmallInteger, nullable=False)
    work_time = Column(INTERVAL)
    probation_time = Column(Date)
    work_type = Column(String(100), nullable=False)
    sign_date = Column(Date, nullable=False)
    employee_id = Column(ForeignKey('employee.id'), nullable=False)

    employee = relationship('Employee', back_populates='contracts')
    position = relationship('Position', back_populates='contracts')


class MedCertificateStatus(enum.Enum):
    opened = 'Открыт'
    continued = 'Продлён'
    closed = 'Закрыт'


class MedicalCertificate(Base):
    __tablename__ = 'medicalcertificate'

    id = Column(Integer, primary_key=True, server_default=text("nextval('medicalcertificate_id_seq'::regclass)"))
    doctor_name = Column(String(150), nullable=False)
    doctor_surname = Column(String(150), nullable=False)
    doctor_lastname = Column(String(150))
    status = Column(Enum(MedCertificateStatus, name='med_certificate_status'), nullable=False)
    ill_time = Column(INTERVAL, nullable=False)
    reason = Column(String(250), nullable=False)
    hospital_name = Column(String(250), nullable=False)
    is_continue = Column(Boolean)
    ogrn = Column(String(13))
    employee_id = Column(ForeignKey('employee.id'))

    employee = relationship('Employee', back_populates='med_certificates')


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, server_default=text("nextval('project_id_seq'::regclass)"))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)
    date_start = Column(Date, nullable=False, server_default=text("now()"))
    date_end = Column(Date)
    contract_id = Column(ForeignKey('contract.number'))
    head_id = Column(ForeignKey('employee.id'))

    contract = relationship('Contract', back_populates='project')
    head = relationship('Employee', back_populates='head_projects')
    
    features = relationship('Feature', back_populates='project')
    employees = relationship('EmployeeProject', back_populates='projects')
    departments = relationship('DepartmentProject', back_populates='projects')


class DepartmentProject(Base):
    __tablename__ = 'departmentproject'
    __table_args__ = (
        UniqueConstraint('project_id', 'department_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('departmentproject_id_seq'::regclass)"))
    project_id = Column(ForeignKey('project.id'), nullable=False)
    department_id = Column(ForeignKey('department.id'), nullable=False)

    departments = relationship('Department', back_populates='projects')
    projects = relationship('Project', back_populates='departments')


class EmployeeProject(Base):
    __tablename__ = 'employeeproject'

    id = Column(Integer, primary_key=True, server_default=text("nextval('employeeproject_id_seq'::regclass)"))
    project_id = Column(ForeignKey('project.id'))
    employee_id = Column(ForeignKey('employee.id'))
    time_periods = Column(ARRAY(INTERVAL()))

    employees = relationship('Employee', back_populates='projects')
    projects = relationship('Project', back_populates='employees')
    
    emprojfeatures = relationship('EmployeeProjectFeature', back_populates='employee_projects')


class Status(enum.Enum):
    opened = 'Открыта'
    onwork = 'В работе'
    closed = 'Закрыта'
    renewed = 'Возобновлена'


class Priority(enum.Enum):
    minor = "Низкий"
    medium = "Средний"
    major = "Срочный"
    critical = "Критический"


class Feature(Base):
    __tablename__ = 'feature'
    __table_args__ = (
        CheckConstraint('date_end > date_start'),
        CheckConstraint('planned_hours > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('feature_id_seq'::regclass)"))
    name = Column(String(150), nullable=False)
    description_id = Column(ForeignKey('description.id'))
    planned_hours = Column(Integer)
    date_start = Column(Date)
    date_end = Column(Date)
    status = Column(Enum(Status, name='status'), nullable=False, server_default=text("'открыта'::status"))
    priority = Column(Enum(Priority, values_callable=lambda obj: [e.value for e in obj]))
    project_id = Column(ForeignKey('project.id'), nullable=False)

    description = relationship('Description', back_populates='features')
    project = relationship('Project', back_populates='features')
    
    mistakes = relationship('Mistake', back_populates='feature')
    tasks = relationship('Task', back_populates='feature')
    emprojfeatures = relationship('EmployeeProjectFeature', back_populates='feature')


class EmployeeProjectFeature(Base):
    __tablename__ = 'employeeprojectfeature'
    __table_args__ = (
        UniqueConstraint('feature_id', 'employeeproj_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('employeeprojectfeature_id_seq'::regclass)"))
    employeeproj_id = Column(ForeignKey('employeeproject.id'), nullable=False)
    feature_id = Column(ForeignKey('feature.id'), nullable=False)

    employee_projects = relationship('EmployeeProject', back_populates='emprojfeatures')
    feature = relationship('Feature', back_populates='emprojfeatures')


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = (
        CheckConstraint('date_end > date_start'),
        CheckConstraint('planned_hours > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('task_id_seq'::regclass)"))
    name = Column(String(150), nullable=False)
    description_id = Column(ForeignKey('description.id'))
    status = Column(Enum(Status, name='status'), nullable=False, server_default=text("'открыта'::status"))
    priority = Column(Enum(Priority, values_callable=lambda obj: [e.value for e in obj]))
    planned_hours = Column(Integer)
    date_start = Column(Date)
    date_end = Column(Date)
    feature_id = Column(ForeignKey('feature.id'))
    employee_id = Column(ForeignKey('employee.id'), nullable=False)

    description = relationship('Description', back_populates='tasks')
    employee = relationship('Employee', back_populates='tasks')
    feature = relationship('Feature', back_populates='tasks')
    
    mistakes = relationship('Mistake', back_populates='task')


class Mistake(Base):
    __tablename__ = 'mistake'
    __table_args__ = (
        CheckConstraint('date_end > date_start'),
        CheckConstraint('planned_hours > 0')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('mistake_id_seq'::regclass)"))
    name = Column(String(150), nullable=False)
    reason_id = Column(ForeignKey('reason.id'))
    description_id = Column(ForeignKey('description.id'), nullable=False)
    status = Column(Enum(Status, name='status'), nullable=False, server_default=text("'открыта'::status"))
    priority = Column(Enum(Priority, values_callable=lambda obj: [e.value for e in obj]))
    planned_hours = Column(Integer)
    date_start = Column(Date)
    date_end = Column(Date)
    feature_id = Column(ForeignKey('feature.id'))
    task_id = Column(ForeignKey('task.id'))
    employee_id = Column(ForeignKey('employee.id'), nullable=False)

    description = relationship('Description', back_populates='mistakes')
    employee = relationship('Employee', back_populates='mistakes')
    feature = relationship('Feature', back_populates='mistakes')
    reason = relationship('Reason', back_populates='mistakes')
    task = relationship('Task', back_populates='mistakes')


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))
    employee_id = Column(ForeignKey('employee.id'))
    employee = relationship('Employee', back_populates='user')

    __table_args__ = (
        UniqueConstraint('name', 'password'),
    )
