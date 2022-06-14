from sqlalchemy import create_engine

engine = create_engine("postgresql://projman:postgrespass@postgresql-projman.alwaysdata.net:5432/projman_database")