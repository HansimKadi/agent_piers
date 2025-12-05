from ..DTOs.eventstate import EventState, EventImageCreate
from ..db.database import SessionLocal
from ..db.crud import create_event, get_all_events, create_image, update_event


# Saves output EventState object from AI to database

def b_save_ai_generated_event(event_state: EventState):
    db = SessionLocal()
    try:

        saved_event = create_event(db, event_state)
        return saved_event
    finally:
        db.close()


# Read all events from database
def debug_read_all_events():
    db = SessionLocal()
    try:
        all_events = get_all_events(db)
        return all_events
    finally:
        db.close()





# Save image DTO in DB
def save_event_image(image_data: EventImageCreate):
    db = SessionLocal()
    try:
        saved_event = create_image(db, image_data)
        return saved_event
    finally:
        db.close()


def save_ai_generated_event(event_state: EventState):
    db = SessionLocal()
    try:
        if event_state.eventid is None: # meaning this is a new event to be created add it to the db then get the id and insert it back into the event state
        
            saved_event = create_event(db, event_state)
            event_state.eventid = saved_event.id
            return saved_event
        
        else:# existing event just update it
            updated_event = update_event(db, event_state)
            return updated_event
    finally:
        db.close()


