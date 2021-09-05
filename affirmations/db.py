from distutils.util import strtobool
import os

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

load_dotenv()


def _cast_boolean(value):
    """
    Helper to convert config values to boolean, got this from:
    https://github.com/henriquebastos/python-decouple/blob/master/decouple.py
    """
    value = str(value)
    return bool(value) if value == "" else bool(strtobool(value))


database_url = os.environ["DATABASE_URL"]
debug = _cast_boolean(os.environ.get("DEBUG", False))

engine = create_engine(database_url, echo=debug)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
