from ..DTOs.eventstate import EventState

"""
Here is where the dynamic dashboard which will help the agent visualize event details will be implemented.



"""

# add conversation history to strengthen context
class Dashboard:
    @staticmethod
    def render(EventState: EventState) -> str:
       """
        Takes the raw state object and converts it into a 
        Markdown-formatted dashboard for the AI System Prompt.
        """
       data = EventState.model_dump() # Get the dictionary representation of the EventState
       missing = EventState.missing_fields() # Get the list of missing fields
       if missing:
           action = f"your next action is to ask the user for the following missing details: {missing}"
           status = "Incomplete"
       else:
           action = "All event details are complete. The event has been saved in the database, stand by for changes or new event creation."
           status = "Complete"
       
       dashboard_text = f"""
        
        # ================= LIVE SYSTEM DASHBOARD =================
        # This section overrides all previous context.
        
        ### CURRENT DATA
        - Name:         {data.get('event_name') or "(MISSING)"}
        - Date:         {data.get('event_date') or "(MISSING)"}
        - Time:         {data.get('event_time') or "(MISSING)"}
        - Location:     {data.get('event_location') or "(MISSING)"}
        
        ### STATUS
        {status}
        Missing Fields: {missing}
        
        ### INSTRUCTION
        {action}
        
        # =========================================================
        """
        
       return dashboard_text