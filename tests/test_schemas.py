from pyrulefilter.schemas import RuleSetType, Rule, RuleSet, OperatorsEnum


def test_Rule_schema():
    s = Rule.model_json_schema()
    assert s["properties"]["categories"]["default"] == []


def test_Rule_null_category():
    r = Rule(
        categories=None, parameter="a", value="b", operator=OperatorsEnum.BeginsWith
    )

    assert r.categories == []
