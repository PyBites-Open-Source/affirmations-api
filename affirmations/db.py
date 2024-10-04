from decouple import config
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = config("DATABASE_URL")
DEBUG = config("DEBUG", default=False, cast=bool)

# heroku does not let me set the DATABASE_URL with the postgresql:// scheme
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=DEBUG)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
