from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    name: str
    handle: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    affirmations: List["Affirmation"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all,delete"}
    )


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class AffirmationBase(SQLModel):
    text: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Affirmation(AffirmationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="affirmations")


class AffirmationCreate(AffirmationBase):
    pass


class AffirmationRead(AffirmationBase):
    id: int
