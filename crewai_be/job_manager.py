from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock
from utils.logging import logger

# Define a lock for thread safety
jobs_lock = Lock()

# Initialize a dictionary to store job information
jobs: Dict[str, "Job"] = {}

# Define the Event data class
@dataclass
class Event:
    timestamp: datetime
    data: str

# Define the Job data class
@dataclass
class Job:
    status: str
    events: List[Event]
    result: str

# Function to append an event to a job
def append_event(job_id: str, event_data: str):
    with jobs_lock:
        if job_id not in jobs:
            # If the job ID is not present, create a new job
            logger.info("Job %s started", job_id)
            jobs[job_id] = Job(
                status='STARTED',
                events=[],
                result='')
        else:
            # If the job ID is present, append the event to the existing job
            logger.info("Appending event for job %s: %s", job_id, event_data)
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data=event_data))
