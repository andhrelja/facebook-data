from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime
)

from config import Base


class Location(Base):
    __tablename__ = 'locations'

    id        = Column(Integer, primary_key=True, autoincrement=True)
    name      = Column(String(255))
    latitude  = Column(Numeric)
    longitude = Column(Numeric)
    timestamp  = Column(DateTime)

    def __repr__(self):
        return "<Location (name={})>".format(self.name)

    def __str__(self):
        return "<Location (name={})>".format(self.name)
