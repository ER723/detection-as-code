"""
Lightweight Sigma rule evaluator for test purposes.

This is NOT a full SIEM query engine — it's an honest, minimal evaluator
that implements just enough of the Sigma detection spec (field modifiers:
equality, contains, endswith; list values as OR; multiple fields in a
block as AND; simple boolean conditions) to prove selection-logic
correctness against sample log fixtures. Real deployment still goes
through sigma-cli to a real backend (Splunk/Elastic/etc) — this harness
tests the detection LOGIC, not full-scale query execution.
"""

import re


def _field_matches(field_raw, expected, log):
    if "|" in field_raw:
        field, modifier = field_raw.split("|", 1)
    else:
        field, modifier = field_raw, None

    actual = log.get(field)
    if actual is None:
        return False

    expected_list = expected if isinstance(expected, list) else [expected]

    for exp in expected_list:
        if modifier == "contains":
            if str(exp).lower() in str(actual).lower():
                return True
        elif modifier == "endswith":
            if str(actual).lower().endswith(str(exp).lower()):
                return True
        elif modifier == "startswith":
            if str(actual).lower().startswith(str(exp).lower()):
                return True
        else:
            if str(actual) == str(exp):
                return True
    return False


def _block_matches(block, log):
    # All fields within a block must match (AND semantics)
    return all(_field_matches(field, value, log) for field, value in block.items())


def evaluate(rule, log):
    """Evaluate a parsed Sigma rule dict against a single log fixture dict."""
    detection = rule["detection"]
    condition_str = detection["condition"]

    block_results = {
        name: _block_matches(block, log)
        for name, block in detection.items()
        if name != "condition"
    }

    # Safe: condition_str comes only from our own rule files, not external input.
    expr = condition_str
    for name in sorted(block_results, key=len, reverse=True):
        expr = re.sub(rf"\b{re.escape(name)}\b", str(block_results[name]), expr)
    expr = expr.replace(" and ", " and ").replace(" not ", " not ")

    return eval(expr)
