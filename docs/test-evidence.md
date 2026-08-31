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

## 2. CI proof without needing to sign in

GitHub requires a free account to view detailed Actions logs, even on public repos — this is a GitHub platform policy, not something specific to this repo. Two things work around that, visible to anyone with zero clicks:

- The badge at the top of this README — a live, auto-updating pass/fail image
- [`docs/sample-test-run.txt`](sample-test-run.txt) — the actual real pytest output, committed as plain text, readable by anyone

## 3. How to reproduce locally

Anyone can independently verify this themselves, not just trust the CI badge:

```bash
git clone https://github.com/ER723/detection-as-code.git
cd detection-as-code
pip install pyyaml pytest
pytest tests/ -v
```

Expected output: 6 passed.
