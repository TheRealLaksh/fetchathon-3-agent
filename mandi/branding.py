"""Agentverse profile details (README with the Innovation Lab badges, description, images) for each agent."""
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
RAW = "https://raw.githubusercontent.com/TheRealLaksh/fetchathon-3-agent/main/assets/"


def profile_kwargs(readme_file: str, description: str) -> dict:
    """Keyword arguments for uagents.Agent. An absolute readme path works from any working directory."""
    return {
        "readme_path": str(DOCS / readme_file),
        "description": description,
        "avatar_url": RAW + "pfp.png",
        "banner_url": RAW + "banner.png",
    }
