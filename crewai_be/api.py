# Standard library imports
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

# Related third-party imports
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Local application/library specific imports
from crew import CompanyResearchCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger

from web_read import get_response, get_vectorstore_from_url

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def kickoff_crew(job_id, companies: list[str], positions: list[str]):
    # Begin the crew kickoff process for the job with ID and specified positions
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        # Create a new crew and set it up with the companies and positions
        company_research_crew = CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(
            companies, positions)
        # Start executing the crew job
        results = company_research_crew.kickoff()

        # Log when the crew job is complete
        logger.info(f"Crew for job {job_id} is complete", results)
        
    except Exception as e:
        # Log if there is an error in the crew kickoff process
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        # Append the error event to the job's event list
        append_event(job_id, f"An error occurred: {e}")
        # Mark the job as error and save the error information
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    # Mark the job as complete and update the result
    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        # Add the completion event to the job's event list
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


@app.route('/api/crew', methods=['POST'])
def run_crew():
    # Handle the request to start the crew job
    logger.info("Received request to run crew")
    # Validate and confirm the provided input data
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")

    # Create a new job ID and get company and position information from the input data
    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']

    # Start a new thread to execute the crew job
    thread = Thread(target=kickoff_crew, args=(
        job_id, companies, positions))
    thread.start()

    # Return the new job ID and accepted status code (202)
    return jsonify({"job_id": job_id}), 202


@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    # View the status of the job with the given ID
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            # If the job is not found, return error code 404
            abort(404, description="Job not found")

    # Convert the job result to JSON format and return
    try:
        result_json = json.loads(job.result)
    except json.JSONDecodeError:
        # If JSON parsing fails, use the original job result
        result_json = job.result

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })


@app.route('/api/answer_question', methods=['POST'])
def answer_question():
    logger.info("Received request to run chat website")
    # Handle the request to answer a question based on content from a blog URL
    job_id = request.json['job_id'] if 'job_id' in request.json else None
    user_query = request.json['user_query']

    # Create a vectorstore from URL if available
    vector_store = None
    
    extracted_urls = []

    if job_id:
        try:
            # Call the `get_status` endpoint to retrieve job information
            response = requests.get(f"http://localhost:3001/api/crew/{job_id}")
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            if response.status_code == 200:
                print("Successful response received!")
                job_data_str = response.text
                try:
                    job_data = json.loads(job_data_str)
                    # ... proceed with extracting URLs from job_data ...
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON data: {e}")
            
            if 'result' in job_data and 'positions' in job_data['result']:
                for position in job_data['result']['positions']:
                    extracted_urls.extend(position.get('blog_articles_urls', []))
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching job information for ID {job_id}: {e}")

    vector_store = get_vectorstore_from_url(extracted_urls)
    # Generate a response using vectorstore and user input, potentially considering extracted URLs
    answer = get_response(user_query, vector_store)
    
    return jsonify({'answer': answer}), 202


if __name__ == '__main__':
    app.run(debug=True, port=3001)

