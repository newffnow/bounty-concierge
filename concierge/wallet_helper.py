"""Wallet operations via the RustChain node API.

Provides balance checks, wallet existence checks, pending transfer lookups,
name validation, and registration guidance for bounty hunters.
"""

import re

import requests

from concierge.config import RUSTCHAIN_NODE_URL

# All requests to the self-signed node use verify=False.
_VERIFY = False
_TIMEOUT = 10

_WALLET_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{1,62}[a-z0-9]$")


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def _get(path, params=None):
    """Issue a GET to the RustChain node, returning parsed JSON or error dict."""
    url = f"{RUSTCHAIN_NODE_URL}{path}"
    try:
        resp = requests.get(url, params=params, verify=_VERIFY, timeout=_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        return {"error": f"Could not connect to node at {RUSTCHAIN_NODE_URL}"}
    except requests.Timeout:
        return {"error": "Request to node timed out (10s)"}
    except requests.RequestException as exc:
        return {"error": f"Request failed: {exc}"}
    except ValueError:
        return {"error": "Node returned non-JSON response"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_wallet_name(name):
    """Validate a proposed wallet name.

    Rules:
        - 3 to 64 characters
        - Lowercase alphanumeric and hyphens only
        - Must start and end with a letter or digit (not a hyphen)

    Args:
        name: Proposed wallet name string.

    Returns:
        (is_valid, message) tuple.
    """
    if not name:
        return (False, "Wallet name cannot be empty.")
    if len(name) < 3:
        return (False, "Wallet name must be at least 3 characters.")
    if len(name) > 64:
        return (False, "Wallet name must be 64 characters or fewer.")
    if name != name.lower():
        return (False, "Wallet name must be lowercase.")
    if not _WALLET_NAME_RE.match(name):
        return (
            False,
            "Wallet name may only contain lowercase letters, digits, and "
            "hyphens, and must start and end with a letter or digit.",
        )
    return (True, "Valid wallet name.")


def check_wallet_exists(name):
    """Check whether a wallet already exists on the RustChain node.

    Sends GET https://50.28.86.131/balance?miner_id=NAME and inspects the
    response.  A wallet exists if the node returns balance data without an
    error.

    Args:
        name: The wallet / miner identifier string.

    Returns:
        True if the wallet exists, False otherwise.
    """
    result = _get("/balance", params={"miner_id": name})
    if "error" in result:
        return False
    # A zero balance still means the wallet entry exists.
    return True


def get_balance(name):
    """Return the RTC balance for a given wallet / miner ID.

    Args:
        name: The miner or wallet identifier string.

    Returns:
        Parsed JSON dict from the node, e.g.
        ``{"miner_id": "...", "balance_rtc": 42.5}``
        or an error dict on failure.
    """
    return _get("/balance", params={"miner_id": name})


def get_pending_transfers(name):
    """Check the /wallet/pending endpoint for pending transfers.

    Args:
        name: The wallet / miner identifier string.

    Returns:
        A list of pending transfer dicts, or an empty list on error.
    """
    result = _get("/wallet/pending", params={"miner_id": name})
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        if "error" in result:
            return []
        return result.get("pending", [])
    return []


def register_wallet_guide(name):
    """Print instructions for registering a new wallet.

    Args:
        name: The desired wallet name.

    Returns:
        Multi-line instruction string.
    """
    valid, msg = validate_wallet_name(name)
    if not valid:
        return f"Invalid wallet name '{name}': {msg}"

    return (
        f"Wallet registration for: {name}\n"
        f"\n"
        f"Option 1 -- Claim a bounty (automatic registration)\n"
        f"  Comment on any bounty issue on GitHub with:\n"
        f"    \"I would like to claim this bounty. Wallet: {name}\"\n"
        f"  Your wallet is registered when the first RTC transfer is made.\n"
        f"\n"
        f"Option 2 -- Install the RustChain Wallet GUI\n"
        f"  Download the .deb package or PyInstaller binary from the\n"
        f"  rustchain-bounties repo releases.  The wallet generates a\n"
        f"  BIP39 seed phrase and Ed25519 keypair automatically.\n"
        f"\n"
        f"Option 3 -- Open a registration issue\n"
        f"  Create an issue on Scottcjn/rustchain-bounties titled:\n"
        f"    \"Wallet Registration: {name}\"\n"
        f"  An admin will set up your wallet entry.\n"
    )


# ---------------------------------------------------------------------------
# Legacy aliases (backwards compatibility)
# ---------------------------------------------------------------------------

def check_balance(wallet_id):
    """Alias for get_balance(). Kept for backwards compatibility."""
    return get_balance(wallet_id)


def check_eligibility(wallet_id):
    """Check lottery / epoch eligibility for a wallet.

    Args:
        wallet_id: The miner or wallet identifier string.

    Returns:
        Parsed JSON dict from the node, or an error dict.
    """
    return _get("/lottery/eligibility", params={"miner_id": wallet_id})


def registration_instructions(name):
    """Alias for register_wallet_guide(). Kept for backwards compatibility."""
    return register_wallet_guide(name)
