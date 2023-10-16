import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from .base import Base


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    city_id = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
