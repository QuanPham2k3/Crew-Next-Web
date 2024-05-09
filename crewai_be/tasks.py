from crewai import Task, Agent
from textwrap import dedent

from search_manager import append_event
from models import SearchInfo, SearchInfoList
from utils.logging import logger

class TopicResearchTasks():

    def __init__(self, search_id):
        self.search_id = search_id

    def append_event_callback(self, task_output):
        # Callback function to append task output to the job's event list
        logger.info("Callback called: %s", task_output)
        append_event(self.search_id, task_output.exported_output)

    def manage_research(self, agent: Agent, topics: list[str], categories: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f"""Leveraging the list of topics {topics} and categories {categories}, 
                               utilize the Research Agent's findings to investigate each category within each 
                               topic. Generate an output in the form of a JSON object containing URLs of 1 to 3 
                               most reputable websites related to each topic for each category.                  
                """),
            agent=agent,
            expected_output=dedent(
                """The Research Agent, responsible for gathering information and providing relevant URLs
                """),
            callback=self.append_event_callback,
            context=tasks,
            output_json=SearchInfoList
        )

    def topic_research(self, agent: Agent, topic: str, categories: list[str]):
        return Task(
            description=dedent(f"""Search for each category {categories} for the topic {topic}. 
                               For each category, find URLs of 1 to 3 websites for each topic. 
                               Return the collected information in a JSON object.
                               
                Guidelines:
                - Search for topic names and URLs, searching on Google with the topic:
                "{topic} [category here] website"
                
                Important Considerations:
                - Once you find information, stop searching immediately to gather more information.
                - Only return the requested results. NOTHING ELSE!
                - Do not create fake information. Only return the results found. Nothing else!
                - Do not stop searching until you find the requested information for each topic.
                """),
            agent=agent,
            expected_output="""A JSON object containing the search information for each topic in each category.""",
            callback=self.append_event_callback,
            output_json=SearchInfo,
            async_execution=True
        )
