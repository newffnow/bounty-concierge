# Contributing to Bounty Concierge

Thanks for your interest in improving the RustChain Bounty Concierge.

## Setup

```bash
git clone https://github.com/Scottcjn/bounty-concierge.git
cd bounty-concierge
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Fork, Branch, PR Workflow

1. Fork the repository on GitHub.
2. Create a branch with a descriptive name:
   - `fix/skill-matcher-scoring`
   - `feat/devto-announcer`
   - `docs/faq-wallet-setup`
3. Make your changes.  Keep each PR focused on one logical change.
4. Push your branch and open a Pull Request against `main`.
5. Reference any related bounty issue in your PR description.

## Code Style

- **Python 3.9+** minimum.  Use features available in 3.9 and above.
- **Type hints encouraged** on function signatures and return types.
- Formatter: **black** (default settings).
- Keep imports sorted: stdlib, third-party, local.
- No emojis in code or docs.
- Docstrings on all public functions and classes.

## Running Tests

```bash
python -m pytest tests/
```

Tests are written with **pytest**.  New functionality should include
corresponding test coverage when practical.

## What We Especially Welcome

- **New FAQ entries** in `docs/` -- common questions from bounty hunters.
- **Skill tag improvements** -- expand `data/skill_tags.json` with more
  keywords so the matcher recommends bounties more accurately.
- **Platform integrations** -- wire up new posting targets in
  `concierge/announcer.py` (4claw, AgentChan, Dev.to, Twitter).
- **Bug fixes** -- if `concierge browse` or `concierge wallet` misbehaves,
  file an issue or send a PR.

## Bounties for Concierge Improvements

Improvements to the concierge tool itself are eligible for RTC bounties.
Check the open issues on
[Scottcjn/rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties/issues)
for tagged concierge tasks, or propose your own enhancement as a new issue.

## Reporting Bugs

Use the [Bug Report](https://github.com/Scottcjn/bounty-concierge/issues/new?template=bug_report.yml)
issue template.

## License

By contributing you agree that your contributions will be licensed under the
MIT License (see [LICENSE](LICENSE)).
