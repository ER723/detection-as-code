# Contributing

This is a personal portfolio project demonstrating detection-engineering methodology (Sigma rules + automated testing). Not actively seeking external contributions, but genuinely open to them.

## Setup
```bash
git clone https://github.com/ER723/detection-as-code.git
cd detection-as-code
pip install -r requirements.txt
```

## Running tests
```bash
pytest tests/ -v
```

## Adding a new rule
1. Add the Sigma rule to `rules/`
2. Add a matching fixture file to `tests/fixtures/` with at least one true-positive and one true-negative case
3. Run `pytest tests/ -v` to confirm it passes
4. Open a PR

## Code style
Formatted and linted with `ruff` (config in `ruff.toml`). Run `ruff check .` before submitting.
