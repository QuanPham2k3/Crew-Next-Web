
from langchain_openai import ChatOpenAI
from agents import TopicResearchAgents
from search_manager import append_event
from tasks import TopicResearchTasks
from crewai import Crew


class TopicResearchCrew:
    def __init__(self, search_id: str):
        self.search_id = search_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        
    def setup_crew(self, topics: list[str], categories: list[str]):
        # Set up the crew for company research
        agents = TopicResearchAgents()
        tasks = TopicResearchTasks(search_id=self.search_id)

        # Create agents and tasks for each company and position
        research_manager = agents.research_manager(topics, categories)
        topic_research_agent = agents.topic_research_agent()

        topic_research_tasks = [
            tasks.topic_research(topic_research_agent, topic, categories) for topic in topics
        ]

        manage_research_task = tasks.manage_research(
            research_manager, topics, categories, topic_research_tasks)

        # Create the crew with agents and tasks
        self.crew = Crew(
            agents=[research_manager, topic_research_agent],
            tasks=[*topic_research_tasks, manage_research_task],
            verbose=2,
        )

    def kickoff(self):
        # Start the crew task
        if not self.crew:
            append_event(self.search_id, "Crew not set up")
            return "Crew not set up"
        
        append_event(self.search_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.search_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.search_id, f"An error occurred: {e}")
            return str(e)
