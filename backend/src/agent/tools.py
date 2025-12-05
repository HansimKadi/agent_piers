from ..DTOs.eventstate import EventState
 # All functions must have an input and output, even if empty failure to do so will cause errors in Gemini tool calling


def participant_notifier(state: EventState, reason: str="event creation") -> str: # A mock function to simulate notifying participants
    """
    Notifies all participants about important updates or events.
    Returns a success message.

    Args:
        reason (str): The reason for notification. Defaults to "event creation".
    """
    return "Participants notified successfully"

# src/agent/tools.py

def update_event_details(state: EventState, event_name: str = None, event_date: str = None,event_time: str = None,event_location: str = None) -> dict:
    """
    Updates the event details.

    Args:
        event_name (str, optional): The new event name. Defaults to None,
        event_date (str, optional): The new event date. Defaults to None.
        event_time (str, optional): The new event time. Defaults to None.
        event_location (str, optional): The new event location. Defaults to None.
        
    """
    if event_name: state.eventname = event_name
    if event_date: state.eventdate = event_date
    if event_time: state.eventtime = event_time
    if event_location: state.eventlocation = event_location
    return f"updated sucessfully status: success", f"updated: {state.model_dump()}"

def event_state_resetter(state: EventState) -> str:
    """
    Resets the event state to its initial empty state.

    Args:
        event_state (EventState): The current event state to be reset. meaning new event

    Returns:
        str: A message indicating the reset status.
    """
    state.eventid = None
    state.eventname = None
    state.eventdate = None
    state.eventtime = None
    state.eventlocation = None
    state.participants = None
    return "new event started."





tool_registry = {
            "update_event_details": update_event_details,
            "event_state_resetter": event_state_resetter,
            #"participant_notifier": participant_notifier
        }


