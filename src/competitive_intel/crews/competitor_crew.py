from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class CompetitorResearchCrew:
    agents_config = "../config/agents.yaml"
    tasks_config = "../config/tasks.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def competitor_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["competitor_analyst"],
            tools=[SerperDevTool(n_results=10)],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def competitor_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["competitor_research_task"],
            agent=self.competitor_analyst(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )