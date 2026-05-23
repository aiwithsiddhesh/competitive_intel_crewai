import shutil
from pathlib import Path

from dotenv import load_dotenv

from competitive_intel.flow import IntelligenceFlow
from competitive_intel.models import CompetitiveReport

load_dotenv()


def _format_markdown(report: CompetitiveReport, company: str, industry: str) -> str:
    mo = report.market_overview
    lines = [
        f"# Competitive Intelligence Report: {company}",
        f"**Industry:** {industry}\n",
        "## Executive Summary",
        report.executive_summary,
        "\n## Market Overview",
        f"- **Market Size:** {mo.market_size}",
        f"- **Growth Rate:** {mo.growth_rate}",
        f"- **TAM/SAM:** {mo.tam_sam_estimate}",
        "\n**Key Trends:**",
    ]
    for trend in mo.key_trends:
        lines.append(f"- {trend}")

    lines.append("\n## Competitor Profiles")
    for cp in report.competitor_profiles:
        lines.append(f"\n### {cp.name}")
        lines.append(f"- **Strengths:** {', '.join(cp.strengths)}")
        lines.append(f"- **Weaknesses:** {', '.join(cp.weaknesses)}")
        lines.append(f"- **Pricing:** {cp.pricing_model}")
        lines.append(f"- **Market Position:** {cp.market_position}")

    lines.append("\n## Strategic Insights")
    for i, insight in enumerate(report.strategic_insights, 1):
        lines.append(f"{i}. {insight}")

    lines.append("\n## Risk Factors")
    for i, risk in enumerate(report.risk_factors, 1):
        lines.append(f"{i}. {risk}")

    lines.append("\n## Recommendations")
    for i, rec in enumerate(report.recommendations, 1):
        lines.append(f"{i}. {rec}")

    return "\n".join(lines)


def run():
    company = "Notion"
    industry = "Productivity Software"

    flow = IntelligenceFlow()

    viz_dir = Path("flow_visualization")
    viz_dir.mkdir(exist_ok=True)
    temp_dir = Path(flow.plot("flow_visualization.html")).parent
    for f in temp_dir.iterdir():
        shutil.copy(f, viz_dir / f.name)

    flow.kickoff(inputs={
        "company_name": company,
        "industry": industry,
        "competitors": ["Obsidian", "Confluence", "Coda", "Roam Research"],
    })

    report = flow.state.final_report

    md = _format_markdown(report, company, industry)
    Path("reports/competitive_report.md").write_text(md, encoding="utf-8")

    print(md)
    print("\n" + "=" * 60)
    print("Report saved to: reports/competitive_report.md")
    print("Flow visualization: flow_visualization/flow_visualization.html")
    print("=" * 60 + "\n")


def kickoff():
    run()


def plot():
    viz_dir = Path("flow_visualization")
    viz_dir.mkdir(exist_ok=True)
    temp_dir = Path(IntelligenceFlow().plot("flow_visualization.html")).parent
    for f in temp_dir.iterdir():
        shutil.copy(f, viz_dir / f.name)


if __name__ == "__main__":
    run()