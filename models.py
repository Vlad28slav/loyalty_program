"""models for database"""
import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv(override=True)

user = os.getenv("POSTGRES_USER_DB")
password = os.getenv("POSTGRES_PASSWORD_TO_USER")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

connection_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index= True)
    program = Column(String, default='5,100!10,300!20,1000') # format is'AmountToGetBonus,BonusSize!AmountToGetBonus,BonusSize'
    started_at = Column(DateTime, index=True)


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index= True)
    current_amount = Column(Integer, index=True, default=0)
    bonuses = Column(Integer, index=True, default=0)
    seller_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, index=True)


engine = create_engine(connection_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
