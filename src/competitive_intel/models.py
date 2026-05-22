from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class MarketOverview(BaseModel):
    market_size: str
    growth_rate: str
    key_trends: list[str]
    tam_sam_estimate: str


class CompetitorProfile(BaseModel):
    name: str
    strengths: list[str]
    weaknesses: list[str]
    pricing_model: str
    market_position: str


class SynthesisOutput(BaseModel):
    key_insights: list[str]
    market_sentiment: Literal["growth", "competitive"]
    strategic_summary: str


class CompetitiveReport(BaseModel):
    executive_summary: str
    market_overview: MarketOverview
    competitor_profiles: list[CompetitorProfile]
    strategic_insights: list[str]
    risk_factors: list[str]
    recommendations: list[str]


class IntelligenceState(BaseModel):
    company_name: str = ""
    industry: str = ""
    competitors: list[str] = []
    market_data: str = ""
    competitor_data: str = ""
    synthesis: SynthesisOutput | None = None
    strategy_report: str | None = None
    final_report: CompetitiveReport | None = None