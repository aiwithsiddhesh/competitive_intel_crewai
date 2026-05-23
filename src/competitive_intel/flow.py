from crewai.flow.flow import Flow, start, listen, router, and_, or_
from crewai import Agent
from typing import Literal

from competitive_intel.models import IntelligenceState, SynthesisOutput
from competitive_intel.crews.market_crew import MarketResearchCrew
from competitive_intel.crews.competitor_crew import CompetitorResearchCrew
from competitive_intel.crews.strategy_crew import StrategyCrew
from competitive_intel.crews.review_crew import ReviewCrew


class IntelligenceFlow(Flow[IntelligenceState]):

    @start()
    def initialize_research(self) -> None:
        print(f"\n{'='*60}")
        print(f"Starting Competitive Intelligence Analysis")
        print(f"Company:     {self.state.company_name}")
        print(f"Industry:    {self.state.industry}")
        print(f"Competitors: {', '.join(self.state.competitors)}")
        print(f"{'='*60}\n")

    @listen(initialize_research)
    def market_research_node(self) -> None:
        result = MarketResearchCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "industry": self.state.industry,
            }
        )
        self.state.market_data = result.raw

    @listen(initialize_research)
    def competitor_research_node(self) -> None:
        result = CompetitorResearchCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "industry": self.state.industry,
                "competitors": ", ".join(self.state.competitors),
            }
        )
        self.state.competitor_data = result.raw

    @listen(and_(market_research_node, competitor_research_node))
    def synthesize_insights(self) -> None:
        synthesis_agent = Agent(
            role=f"Strategic Intelligence Synthesizer for {self.state.industry}",
            goal=(
                "Synthesize market research and competitor analysis into a structured strategic brief. "
                "Classify market sentiment as exactly 'growth' or 'competitive' with a one-sentence justification."
            ),
            backstory=(
                "You are a strategy consultant who distills complex, multi-source data into executive-ready insights. "
                "You always commit to a definitive sentiment classification backed by evidence from the provided research."
            ),
            verbose=True,
        )

        prompt = (
            f"Analyze the following research for {self.state.company_name} "
            f"in the {self.state.industry} industry and produce a structured strategic synthesis.\n\n"
            f"MARKET RESEARCH:\n{self.state.market_data}\n\n"
            f"COMPETITOR ANALYSIS:\n{self.state.competitor_data}\n\n"
            f"Extract 5-7 key strategic insights, classify market sentiment as 'growth' "
            f"(fast-growing, whitespace, first-mover opportunity) or 'competitive' "
            f"(saturated, differentiation required), and write a strategic summary paragraph."
        )

        result = synthesis_agent.kickoff(prompt, response_format=SynthesisOutput).pydantic
        self.state.synthesis = result

    @router(synthesize_insights)
    def route_by_sentiment(self) -> Literal["growth_opportunity", "competitive_threat"]:
        print(f"\nRouting on sentiment: {self.state.synthesis.market_sentiment}")
        if self.state.synthesis.market_sentiment == "growth":
            return "growth_opportunity"
        return "competitive_threat"

    @listen("growth_opportunity")
    def generate_strategy_report(self) -> None:
        result = StrategyCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "industry": self.state.industry,
                "market_data": self.state.market_data,
                "competitor_data": self.state.competitor_data,
            }
        )
        self.state.strategy_report = result.raw

    @listen("competitive_threat")
    def generate_defense_report(self) -> None:
        result = StrategyCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "industry": self.state.industry,
                "market_data": self.state.market_data,
                "competitor_data": self.state.competitor_data,
            }
        )
        self.state.strategy_report = result.raw

    @listen(or_(generate_strategy_report, generate_defense_report))
    def finalize_report(self) -> None:
        result = ReviewCrew().crew().kickoff(
            inputs={
                "company_name": self.state.company_name,
                "industry": self.state.industry,
                "strategy_report": self.state.strategy_report,
            }
        )
        self.state.final_report = result.pydantic
