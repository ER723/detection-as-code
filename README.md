![Tests](https://github.com/ER723/detection-as-code/actions/workflows/test.yml/badge.svg)

# Detection-as-Code — Tested Sigma Rules with CI

Three vendor-agnostic Sigma detection rules, each covering a distinct, well-documented MITRE ATT&CK technique, with an automated test suite that verifies every rule against real true-positive and true-negative log fixtures on every push.

**This is a standalone project, independent of any specific SIEM or pipeline.** It demonstrates detection-engineering methodology — writing testable detection logic — not the operation of a specific system.

## Why this exists

Most Sigma rules are written once and never verified against real sample data. This repo treats detection rules like source code: version-controlled, tested automatically, with genuine pass/fail evidence — not just claims that a rule "should" work.

## What's tested

| Rule | Technique | True positives | True negatives | Data source |
|---|---|---|---|---|
| `cron_persistence.yml` | T1053.003 — Cron Job Persistence | 1 | 2 | **Genuinely captured real command execution on macOS** — not synthetic. `crontab -e` actually run in a real zsh session, `brew list` actually run, exact captured `CommandLine`/`ParentCommandLine` values used as fixtures. |
| `lsass_access.yml` | T1003.001 — Credential Dumping via LSASS | 2 | 3 (including a legitimate-EDR near-miss) | Schema-accurate synthetic fixtures, modeled on real Sysmon Event ID 10 field structure. Windows-specific technique; no Windows host available. Capturing genuinely real Sysmon data would require a VM, which conflicts with this project's lightest-weight goal — noted honestly rather than left ambiguous. |
| `powershell_encoded_command.yml` | T1059.001 — Encoded PowerShell Execution | 2 | 2 | Same as above — schema-accurate synthetic, same honest reasoning. |

Every "near-miss" fixture exists specifically to prove the rule's filter logic works — not just that it matches obvious cases, but that it correctly *excludes* the specific benign scenarios it's designed to exclude.

## How it's tested

`tests/sigma_evaluator.py` is a small, honestly-scoped evaluator — **not a full SIEM query engine**. It implements enough of the Sigma detection spec (field modifiers, AND/OR/NOT logic) to verify selection logic against fixtures. Real deployment still goes through `sigma-cli` to convert rules to a real backend (Splunk, Elastic, Sentinel, etc.) — this harness tests the *logic*, not full-scale query execution.

```bash
pip install pyyaml pytest
pytest tests/ -v
```

## CI

Every push and pull request runs the full test suite via GitHub Actions — see the badge/checkmark on this repo, or `.github/workflows/test.yml`.

## Relationship to other projects

This is intentionally separate from my [SOC escalation pipeline](https://github.com/ER723/Automated-SOC-Tier-1-to-Tier-2-Escalation-Pipeline) — that project demonstrates building and operating a live detection/response system; this one demonstrates detection-engineering methodology in isolation. Different skills, kept as different projects deliberately.
