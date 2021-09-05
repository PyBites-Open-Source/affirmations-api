import os

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

database_url = os.environ["DATABASE_URL"]
connect_args = {"check_same_thread": False}
engine = create_engine(database_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
