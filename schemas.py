from pydantic import BaseModel


class CustomerBase(BaseModel):

    name: str
    current_amount: int
    bonuses :int
    created_at: str


class CustomerCreate(CustomerBase):

    pass


class Customer(CustomerBase):
    seller_id: int

    class Config:

        orm_mode = True


class UserBase(BaseModel):
    """Creating base for creating user objects"""

    id: int
    program: str
    started_at: str


class UserCreate(UserBase):

    pass


class User(UserBase):

    class Config:

        orm_mode = True