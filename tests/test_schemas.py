from pyrulefilter.schemas import (
    RuleSetType,
    Rule,
    RuleSet,
)


def test_Rule_schema():
    s = Rule.schema()
    assert s["properties"]["categories"]["default"] == []


def test_RuleSet_schema():
    s = RuleSet.schema()
    assert s["title"] == "RuleSet"
