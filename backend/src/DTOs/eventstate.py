# src/DTOs/eventstate.py
from pydantic import BaseModel, Field
from typing import Optional, List

# -- Api request/response models


# --- Pydantic Models ---
class ChatRequest(BaseModel): # the input from the user
    prompt: str


class ChatResponse(BaseModel): # the response from the ai
    response: str


# Event state 
class EventState(BaseModel):
    eventid: Optional[int] = Field(None, description="Unique identifier for the event")
    eventname: Optional[str] = Field(None, description="Name of the event")
    eventdate: Optional[str] = Field(None, description="Date of the event in YYYY-MM-DD format")
    eventtime: Optional[str] = Field(None, description="Time of the event in HH:MM format")
    eventlocation: Optional[str] = Field(None, description="Location of the event")
    participants: Optional[List[str]] = Field(None, description="List of participants' names or emails")

    def missing_fields(self) -> List[str]:
        missing = []
        if not self.eventname:
            missing.append("eventname")
        if not self.eventdate:
            missing.append("eventdate")
        if not self.eventtime:
            missing.append("eventtime")
        if not self.eventlocation:
            missing.append("eventlocation")
        #if not self.participants:
         #   missing.append("participants")
        return missing

    @property # check if all required fields are present
    def is_complete(self) -> bool: 
        #return len(self.missing_fields()) == 0 # if no missing fields, then complete. If any missing, then incomplete
        if len(self.missing_fields()) == 0:
            return "\nAll required event details are present."
        else:
            return "\nSome event details are missing."


# DTO to send to image creation
class EventImageCreate(BaseModel):
    event_id: int = Field(None, description="FK to events table")
    image_bytes: bytes = Field(None, description="Image stored in bytes")