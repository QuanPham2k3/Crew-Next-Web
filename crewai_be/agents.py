from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

class TopicResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        #ChatGroq(model="llama3-8b-8192")

    def research_manager(self, topics: List[str], categoris: List[str]) -> Agent:
        return Agent(
            role="Topic Research Manager",
            goal=f"""Generate a JSON object containing URLs of 1 to 3 most reputable websites related to each topic for each category.
             
                Topics: {topics}
                Categorys: {categoris}

                Important Note:
                - The final JSON must contain all topics for each category.
                - If information cannot be found due to special reasons, fill in the information "MISSING".
                - Do not create fake information. Only return information that is found. Nothing else!
                - Do not stop searching until the search for each topic in each category is complete.
                - Make sure to search for 1 to 3 most reputable websites related to each topic in each category.
                """,
            backstory="""As a Topic Research Manager, you are responsible for maintaining the information search process 
            and ensuring that a list is returned.""",
            llm=self.llm,
            tools=[self.searchInternetTool],
            verbose=True,
            allow_delegation=True,
            #max_rpm = 1
        )

    def topic_research_agent(self) -> Agent:
        return Agent(
            role="Topic Research Agent",
            goal="""Search for information based on the topic of each category and return 1-3 website URLs for each. 
            Your job is to search for information and return it in JSON object format.""",
            backstory="""As a Topic Research Agent, you are responsible for searching for information based on the topic of each category and 
            returning 1-3 website URLs for each.
                
                Important Considerations:
                - Stop searching immediately once you have found the information.
                - Only return the requested information. NOTHING ELSE!
                - Make sure to search for each topic in each category.
                - Do not create fake information. Only return information that is found. Nothing else!
                """,
            tools=[self.searchInternetTool],
            llm=self.llm,
            verbose=True,
            #max_rpm = 1
        )

  