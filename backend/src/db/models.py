from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from .database import Base
from sqlalchemy.types import JSON

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    eventname = Column(String, nullable=True)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    location = Column(String, nullable=True)

    # Participants stored as a JSON list - this is for simplicity
    # Will be changed with relationships later
    participants = Column(JSON, nullable=True)

    # Convert to dict for printing
    def to_dict(self):
        return {
            "id": self.id,
            "eventname": self.eventname,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "participants": self.participants,
        }


class EventImage(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    image = Column(LargeBinary, nullable=False)
