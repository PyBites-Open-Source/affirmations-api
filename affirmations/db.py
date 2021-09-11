from decouple import config
from sqlmodel import SQLModel, create_engine

DATABASE_URL = config("DATABASE_URL")
DEBUG = config("DEBUG", default=False, cast=bool)


engine = create_engine(DATABASE_URL, echo=DEBUG)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
