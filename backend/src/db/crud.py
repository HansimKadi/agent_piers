from sqlalchemy.orm import Session
from ..DTOs.eventstate import EventState, EventImageCreate
from .models import Event, EventImage


def create_event(db: Session, event_data: EventState):
    db_event = Event(
        eventname = event_data.eventname,
        date = event_data.eventdate,
        time = event_data.eventtime,
        location = event_data.eventlocation,
        participants = event_data.participants
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event




def get_all_events(db: Session):
    return db.query(Event).all()


def create_image(db: Session, image_data: EventImageCreate):
    db_image = EventImage(
        event_id = image_data.event_id,
        image = image_data.image_bytes
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image

def update_event(db: Session, event_state: EventState):
    # 1. Retrieve the existing record from DB
    db_event = db.query(Event).filter(Event.id == event_state.eventid).first()
    
    if db_event:
        # 2. Update fields (Map your state to the DB model)
        db_event.eventname = event_state.eventname
        db_event.time = event_state.eventtime
        db_event.location = event_state.eventlocation
        db_event.date = event_state.eventdate
        # ... map other fields here ...

        # 3. Commit the changes
        db.commit()
        db.refresh(db_event) # Refresh to get any DB-side changes (like updated_at timestamps)
        return db_event
    else:
        # Edge case: ID exists in state, but row missing in DB (deleted?)
        # You might want to handle this by creating it instead, or raising error
        raise ValueError(f"Event with ID {event_state.eventid} not found.")
