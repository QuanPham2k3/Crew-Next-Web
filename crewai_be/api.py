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
from crew import TopicResearchCrew
from search_manager import append_event, searchs, searchs_lock, Event
from utils.logging import logger

from url_read import get_response, get_vectorstore_from_url

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def kickoff_crew(search_id, topics: list[str],categories: list[str]):
    # Begin the crew kickoff process for the search with ID and specified positions
    logger.info(f"Crew for search {search_id} is starting")

    results = None
    try:
        # Create a new crew and set it up with the companies and positions
        topic_research_crew = TopicResearchCrew(search_id)
        topic_research_crew.setup_crew(
                topics, categories)
        # Start executing the crew search
        results = topic_research_crew.kickoff()

        # Log when the crew search is complete
        logger.info(f"Crew for search {search_id} is complete", results)
        
    except Exception as e:
        # Log if there is an error in the crew kickoff process
        logger.error(f"Error in kickoff_crew for search {search_id}: {e}")
        # Append the error event to the search's event list
        append_event(search_id, f"An error occurred: {e}")
        # Mark the search as error and save the error information
        with searchs_lock:
            searchs[search_id].status = 'ERROR'
            searchs[search_id].result = str(e)

    # Mark the search as complete and update the result
    with searchs_lock:
        searchs[search_id].status = 'COMPLETE'
        searchs[search_id].result = results
        # Add the completion event to the search's event list
        searchs[search_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


@app.route('/api/crew', methods=['POST'])
def run_crew():
    # Handle the request to start the crew search
    logger.info("Received request to run crew")
    # Validate and confirm the provided input data
    data = request.json
    if not data or 'topics' not in data or 'categories' not in data:
        abort(400, description="Invalid input data provided.")

    # Create a new search ID and get company and position information from the input data
    search_id = str(uuid4())
    topics = data['topics']
    categories = data['categories']

    # Start a new thread to execute the crew search
    thread = Thread(target=kickoff_crew, args=(
        search_id, topics, categories))
    thread.start()

    return jsonify({"search_id": search_id}), 202


@app.route('/api/crew/<search_id>', methods=['GET'])
def get_status(search_id):
    # View the status of the search with the given ID
    with searchs_lock:
        search = searchs.get(search_id)
        if search is None:
            # If the search is not found, return error code 404
            abort(404, description="search not found")

    # Convert the search result to JSON format and return
    try:
        result_json = json.loads(search.result)
    except json.JSONDecodeError:
        # If JSON parsing fails, use the original search result
        result_json = search.result

    return jsonify({
        "search_id": search_id,
        "status": search.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in search.events]
    })


@app.route('/api/answer_question', methods=['POST'])
def answer_question():
    logger.info("Received request to run chat website")
    # Handle the request to answer a question based on content from a blog URL
    search_id = request.json['search_id'] if 'search_id' in request.json else None
    user_query = request.json['user_query']

    # Create a vectorstore from URL if available
    vector_store = None
    
    extracted_urls = []

    if search_id:
        try:
            # Call the `get_status` endpoint to retrieve search information
            response = requests.get(f"http://localhost:3001/api/crew/{search_id}")
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            if response.status_code == 200:
                print("Successful response received!")
                search_data_str = response.text
                try:
                    search_data = json.loads(search_data_str)
                    # ... proceed with extracting URLs from search_data ...
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON data: {e}")
            
            if 'result' in search_data and 'searchs' in search_data['result']:
                for url_search in search_data['result']['searchs']:
                    extracted_urls.extend(url_search.get('web_urls', []))
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching search information for ID {search_id}: {e}")

    vector_store = get_vectorstore_from_url(extracted_urls)
    # Generate a response using vectorstore and user input, potentially considering extracted URLs
    answer = get_response(user_query, vector_store)
    
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True, port=3001)

