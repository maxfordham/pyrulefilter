from pyrulefilter.schemas import (
    RuleSetType,
    Rule,
    RuleSet,
)


def test_Rule_schema():
    s = Rule.model_json_schema()
    assert s["properties"]["categories"]["default"] is None


def test_RuleSet_schema():
    s = RuleSet.model_json_schema()
    assert s["title"] == "Rule Set Definition"
