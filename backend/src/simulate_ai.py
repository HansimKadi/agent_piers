# ----- SCRIPT TO SIMULATE RESPONSE FROM AI -----
from .DTOs.eventstate import EventState, EventImageCreate
from .ai.event_handler import save_ai_generated_event, debug_read_all_events, save_event_image
import os


def simulate_ai_event():
    fake_event = EventState(
        eventname="Redbull cliff diving",
        eventdate="2025-12-02",
        eventtime="19:00",
        eventlocation="Kragerø",
        participants=["amund", "shefat", "hansim"]
    )

    print("Simulating AI event creation...")

    # Save to db
    saved_event = save_ai_generated_event(fake_event)
    print("\nSaved event:", saved_event, sep="\n")

    # Read from db
    print("\nReading all event from DB:")
    all_events = debug_read_all_events()
    for event in all_events:
        print(event.to_dict())

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "test_image.jpeg")

    print("\nTrying to save test image...")
    print("Looking for:", image_path)

    with open(image_path, "rb") as test_image:
        image_bytes = test_image.read()

    fake_image = EventImageCreate(
        event_id=1,
        image_bytes=image_bytes
    )
    saved_image = save_event_image(fake_image)

if __name__ == "__main__":
    simulate_ai_event()
