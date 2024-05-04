from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock
from utils.logging import logger

# Define a lock for thread safety
searchs_lock = Lock()

# Initialize a dictionary to store search information
searchs: Dict[str, "Search"] = {}

# Define the Event data class
@dataclass
class Event:
    timestamp: datetime
    data: str

# Define the Search data class
@dataclass
class Search:
    status: str
    events: List[Event]
    result: str

# Function to append an event to a job
def append_event(search_id: str, event_data: str):
    with searchs_lock:
        if search_id not in searchs:
            # If the search ID is not present, create a new search
            logger.info("Search %s started", search_id)
            searchs[Dict] = Search(
                status='STARTED',
                events=[],
                result='')
        else:
            # If the search ID is present, append the event to the existing search
            logger.info("Appending event for topic %s: %s", search_id, event_data)
        
        searchs[search_id].events.append(
            Event(timestamp=datetime.now(), data=event_data))
