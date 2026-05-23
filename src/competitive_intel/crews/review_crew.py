from typing import Any, Tuple

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from competitive_intel.models import CompetitiveReport


def validate_report_completeness(result) -> Tuple[bool, Any]:
    report = result.pydantic

    if not isinstance(report, CompetitiveReport):
        return (False, "Output could not be parsed as CompetitiveReport")

    missing = []

    if not report.executive_summary.strip():
        missing.append("executive_summary")
    if not report.market_overview:
        missing.append("market_overview")
    if not report.competitor_profiles:
        missing.append("competitor_profiles")
    if len(report.strategic_insights) < 5:
        missing.append(f"strategic_insights (found {len(report.strategic_insights)}, need 5)")
    if len(report.risk_factors) < 3:
        missing.append(f"risk_factors (found {len(report.risk_factors)}, need 3)")
    if not report.recommendations:
        missing.append("recommendations")

    if missing:
        return (False, f"Report incomplete — missing or insufficient: {', '.join(missing)}")

    return (True, report)


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
            agent=self.report_writer(),
            output_pydantic=CompetitiveReport,
            guardrail=validate_report_completeness,
            guardrail_max_retries=3,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.report_writer(), self.fact_checker()],
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.senior_analyst(),
            verbose=True,
        )