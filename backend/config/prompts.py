"""Utility for loading prompts from the prompts/ directory."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def load_prompt(name: str) -> str:
    """Loads a prompt from a .txt file by name."""
    file_path = PROMPTS_DIR / f"{name}.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    return file_path.read_text().strip()
