from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://projman:postgrespass@postgresql-projman.alwaysdata.net:5432/projman_database")

session = Session(engine)
