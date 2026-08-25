"""
Detection-as-code test suite.

Loads every rule in rules/*.yml and its matching fixture file in
tests/fixtures/, asserting each true-positive fixture fires the rule
and each true-negative fixture does not. Run with: pytest tests/
"""

import json
import os
import yaml
import pytest
from sigma_evaluator import evaluate

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "rules")
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def load_rule_fixture_pairs():
    pairs = []
    for filename in os.listdir(RULES_DIR):
        if not filename.endswith(".yml"):
            continue
        rule_name = filename[:-4]
        rule_path = os.path.join(RULES_DIR, filename)
        fixture_path = os.path.join(FIXTURES_DIR, f"{rule_name}.json")
        if not os.path.exists(fixture_path):
            continue
        with open(rule_path) as f:
            rule = yaml.safe_load(f)
        with open(fixture_path) as f:
            fixtures = json.load(f)
        pairs.append((rule_name, rule, fixtures))
    return pairs


@pytest.mark.parametrize(
    "rule_name,rule,fixtures",
    load_rule_fixture_pairs(),
    ids=lambda x: x if isinstance(x, str) else "",
)
def test_true_positives_fire(rule_name, rule, fixtures):
    for case in fixtures.get("true_positives", []):
        result = evaluate(rule, case["log"])
        assert result is True, (
            f"[{rule_name}] Expected MATCH for true positive '{case['name']}' "
            f"but rule did not fire."
        )


@pytest.mark.parametrize(
    "rule_name,rule,fixtures",
    load_rule_fixture_pairs(),
    ids=lambda x: x if isinstance(x, str) else "",
)
def test_true_negatives_do_not_fire(rule_name, rule, fixtures):
    for case in fixtures.get("true_negatives", []):
        result = evaluate(rule, case["log"])
        assert result is False, (
            f"[{rule_name}] Expected NO MATCH for true negative '{case['name']}' "
            f"but rule fired (false positive)."
        )
