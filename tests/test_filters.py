from pyrulefilter.filters import (
    RuleSetType,
    Rule,
    RuleSet,
)  # , Docum    RuleSet #ScheduleRuleSet,
from pyrulefilter.enums import OperatorsEnum, FilterCategoriesEnum
from pyrulefilter.filters import (
    operate_rule_on_value,
    rule_check_dict,
    ruleset_check_dict,
    ruleset_check_dicts,
)
from pyuniclass import UT


# example1: TypeSpecification from aectemplater (2023-04-25)
# set_type = RuleSetType.AND
# rule = Rule(
#     categories=[],
#     property="OverallHeight",
#     operator=OperatorsEnum.GreaterOrEqual,
#     value=150,
# )
# rule_set = RuleSet(set_type=set_type, rules=[rule])

# example2: pyuniclass
GROUP = "Pr_70_60_36"  # Heat emitters
SUBGROUP = "Pr_70_60_36_73"  #  Radiators
rule1 = Rule(
    categories=[],
    property="ClassificationProductCode",
    operator=OperatorsEnum.BeginsWith,
    value=GROUP,
)
rule2 = Rule(
    categories=[],
    property="ClassificationProductCode",
    operator=OperatorsEnum.NotBeginsWith,
    value=SUBGROUP,
)


def get_typespec(type_spec_id: int) -> dict:
    import requests

    AECTEMPLATER_CNAME = "https://aectemplater.maxfordham.com"
    url = AECTEMPLATER_CNAME + f"/type_spec/{str(type_spec_id)}"
    r = requests.get(url=url)
    return r.json()


class TestRules:
    def test_uniclass(self):
        valid_codes = [
            value for value in UT.Pr.codes if operate_rule_on_value(value, rule1)
        ]
        for v in valid_codes:
            assert GROUP in v
        print("done")

    def test_rule(self):
        data = {"a": "ave a good day"}
        r1 = Rule(property="a", value="ave", operator=OperatorsEnum.BeginsWith)
        assert rule_check_dict(data, r1)

        r1.value = "good"
        assert not rule_check_dict(data, r1)

        r1.operator = OperatorsEnum.Contains
        assert rule_check_dict(data, r1)

        r1.property = "b"
        assert not rule_check_dict(data, r1)

    def test_ruleset(self):
        data = {"a": "ave a good day", "b": "be good"}
        r1 = Rule(property="a", value="ave", operator=OperatorsEnum.BeginsWith)
        r2 = Rule(property="a", value="good", operator=OperatorsEnum.Contains)
        r3 = Rule(property="b", value="good", operator=OperatorsEnum.Contains)
        rule_set = RuleSet(set_type=RuleSetType.AND, rules=[r1, r2, r3])

        assert ruleset_check_dict(data, rule_set)

        r4 = Rule(property="a", value="day", operator=OperatorsEnum.NotContains)
        rule_set = RuleSet(set_type=RuleSetType.AND, rules=[r1, r2, r3, r4])
        check = ruleset_check_dict(data, rule_set)
        assert not check

    def test_array_of_data(self):
        data = [
            {"a": "ave a good day", "b": "be good"},
            {"a": "ave a bad day", "b": "be bad"},
        ]
        r2 = Rule(property="a", value="good", operator=OperatorsEnum.Contains)
        rule_set = RuleSet(set_type=RuleSetType.AND, rules=[r2])

        assert ruleset_check_dicts(data, rule_set) == [True, False]

        r1 = Rule(property="a", value="day", operator=OperatorsEnum.Contains)
        r2 = Rule(property="b", value="be", operator=OperatorsEnum.BeginsWith)
        rule_set = RuleSet(set_type=RuleSetType.AND, rules=[r1, r2])
        check = ruleset_check_dicts(data, rule_set)
        assert check == [True, True]

    def test_type_spec_data_on_server(self):
        # NOTE: THIS WILL ONLY WORK IF THE SERVER IS RUNNING
        li = [15, 16]
        data = [get_typespec(l) for l in li]
        # categories = [l["property_schemas"]["revit_category"] for l in data]
        categories = None
        data = [l["property_data"] for l in data]

        r1 = Rule(
            property="Manufacturer",
            value="Honeywell",
            operator=OperatorsEnum.Contains,
        )
        # r2 = Rule(property="TypeReference", value="2", operator=OperatorsEnum.Greater)
        rule_set = RuleSet(set_type=RuleSetType.AND, rules=[r1])  # , r2

        check = ruleset_check_dicts(data, rule_set, li_categories=categories)
        assert check == [True, False]

    def test_categories(self):
        assert FilterCategoriesEnum.OST_DuctInsulations == "Duct Insulations"
