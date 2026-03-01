"""Configuration module for RustChain Bounty Concierge.

All settings are loaded from environment variables with sensible defaults.
"""

import os


def _env(key, default=""):
    """Read an environment variable, returning default if unset or empty."""
    return os.environ.get(key, default) or default


# --- API tokens (optional -- features degrade gracefully without them) ---

GITHUB_TOKEN = _env("GITHUB_TOKEN")
RC_ADMIN_KEY = _env("RC_ADMIN_KEY")
DEVTO_API_KEY = _env("DEVTO_API_KEY")
GROK_API_KEY = _env("GROK_API_KEY")

# --- RustChain node ---

RUSTCHAIN_NODE_URL = _env("RUSTCHAIN_NODE_URL", "https://50.28.86.131")

# --- Repositories to aggregate bounties from ---

REPOS = [
    "Scottcjn/rustchain-bounties",
    "Scottcjn/Rustchain",
    "Scottcjn/bottube",
    "Scottcjn/beacon-skill",
    "Scottcjn/ram-coffers",
    "Scottcjn/claude-code-power8",
    "Scottcjn/nvidia-power8-patches",
    "Scottcjn/llama-cpp-power8",
    "Scottcjn/grazer-skill",
]

# --- Docs directory (for FAQ doc search) ---

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
