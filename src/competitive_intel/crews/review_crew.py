from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ReviewCrew:
    agents_config = "../config/agents.yaml"
    tasks_config = "../config/tasks.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["report_writer"],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["fact_checker"],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def senior_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_analyst"],
            allow_delegation=True,
            verbose=True,
        )

    @task
    def final_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_review_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.senior_analyst(),
            verbose=True,
        )