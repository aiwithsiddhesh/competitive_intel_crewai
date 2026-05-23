from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class StrategyCrew:
    agents_config = "../config/agents.yaml"
    tasks_config = "../config/tasks.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def strategy_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["strategy_writer"],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def strategy_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["strategy_report_task"],
            agent=self.strategy_writer(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )