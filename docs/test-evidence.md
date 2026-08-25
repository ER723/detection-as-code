**Real test evidence:** [`docs/test-evidence.md`](docs/test-evidence.md)

# Test Evidence

Real, verifiable evidence that the tests in this repo were genuinely executed — not just written and claimed to pass.

## 1. Real command capture (cron_persistence rule)

The `cron_persistence` rule's true-positive fixture is not synthetic. It was captured from an actual command run on a real macOS host:

```
$ crontab -e
crontab: no crontab for [user] - using an empty one
crontab: no changes made to crontab

$ echo "SHELL_IN_USE: $SHELL"
SHELL_IN_USE: /bin/zsh
```

The exact `CommandLine` (`crontab -e`) and `ParentCommandLine` (`/bin/zsh`) values in [`tests/fixtures/cron_persistence.json`](../tests/fixtures/cron_persistence.json) come directly from this real session — not invented.

## 2. Live, publicly-viewable CI run

This isn't a screenshot claim — anyone can click through and see the actual logs, no login required, since this is a public repository:

**[View the live Actions run](https://github.com/ER723/detection-as-code/actions)**

Expand the `test` step in any run to see the real `pytest` output, including every individual test name and its pass/fail result — not just a collapsed "Success" badge.

## 3. How to reproduce locally

Anyone can independently verify this themselves, not just trust the CI badge:

```bash
git clone https://github.com/ER723/detection-as-code.git
cd detection-as-code
pip install pyyaml pytest
pytest tests/ -v
```

Expected output: 6 passed.
