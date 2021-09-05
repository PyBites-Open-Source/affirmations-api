from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    handle: str
    affirmations: List["Affirmation"] = Relationship(back_populates="user")


class Affirmation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="affirmations")
