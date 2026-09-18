# Contributing

This is a personal portfolio project demonstrating detection-engineering methodology (Sigma rules + automated testing). Not actively seeking external contributions, but genuinely open to them — new detection rules, fixture improvements, or corrections are all welcome.

## What's in this repo

Three vendor-agnostic Sigma detection rules, each mapped to a specific MITRE ATT&CK technique, backed by an automated pytest suite that verifies every rule against real true-positive and true-negative log fixtures on every push. The goal is treating detection rules like source code — version-controlled and tested — rather than written once and never verified.

## Setup

```bash
git clone https://github.com/ER723/detection-as-code.git
cd detection-as-code
pip install -r requirements.txt
```

## Code style

Linted and formatted with [ruff](https://docs.astral.sh/ruff/), configured in `ruff.toml`:

```bash
ruff check .
```

CI runs this automatically on every push and pull request — a failing lint check blocks the PR from merging.

## Running tests

```bash
pytest tests/ -v
```

`tests/sigma_evaluator.py` is a small, honestly-scoped evaluator — not a full SIEM query engine — that implements enough of the Sigma detection spec (field modifiers, AND/OR/NOT logic) to verify selection logic against fixtures.

## Adding a new rule

1. Add the Sigma rule to `rules/`, mapped to a specific, well-documented MITRE ATT&CK technique
2. Add a matching fixture file to `tests/fixtures/` with at least one true-positive and one true-negative case. Real captured data is strongly preferred over synthetic where feasible (see `cron_persistence.yml`'s fixture for an example); where synthetic is the only option, keep it schema-accurate and say so explicitly rather than implying it's real
3. Include at least one "near-miss" true-negative — a case that looks similar to the malicious pattern but should specifically *not* fire, proving the rule's filter logic actually discriminates rather than just matching the obvious case
4. Run `pytest tests/ -v` and `ruff check .` — both must pass locally before pushing

## Pull request workflow

1. Fork the repository, or create a branch directly if you have write access: `git checkout -b add/technique-name`
2. Make your change, following the rule-adding steps above for any new detection
3. Confirm both `pytest tests/ -v` and `ruff check .` pass locally
4. Push your branch and open a pull request against `main`
5. CI (tests, linting, CodeQL) runs automatically on the PR — wait for it to go green before requesting a look
6. Once checks pass, the PR can be merged

## Code of conduct

Be specific, be respectful, and back up every claim with evidence — real fixtures over synthetic where possible, honest documentation of any known limitation, and no overstated capability claims. That standard applies to this repo's own content as much as to any contribution.
