from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    
class CompanyResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.webScrapeTool = ScrapeWebsiteTool()

    def research_manager(self, companies: List[str], positions: List[str]) -> Agent:
        return Agent(
            role="Company Research Manager",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles
            ,for each position in each company.
             
                Companies: {companies}
                Positions: {positions}

                Important:
                - The final list of JSON objects must include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each position in each company.
                - All the companies and positions exist so keep researching until you find the information for each one.
                - Make sure you each researched position for each company contains 3 blog articles
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information
                into a list.""",
            llm=self.llm,
            tools=[self.searchInternetTool],
            verbose=True,
            allow_delegation=True
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and find urls for 3 recent blog articles 
                for each person in the specified positions. It is your job to return this collected 
                information in a JSON object""",
            backstory="""As a Company Research Agent, you are responsible for looking up specific positions 
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Make sure you find the persons name who holds the position.
                - Do not generate fake information. Only return the information you find. Nothing else!
                """,
            tools=[self.searchInternetTool],
            llm=self.llm,
            verbose=True
        )

  