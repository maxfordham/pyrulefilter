from pyrulefilter.schemas import Rule, RuleSet
from pyrulefilter.enums import FilterCategoriesEnum, OperatorsEnum, RuleSetType
from pyrulefilter.operators import MAP_OPERATORS
import typing as ty
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "Rule",
    "RuleSet",
    "RuleSetType",
    "FilterCategoriesEnum",
    "OperatorsEnum",
]

def get_param_value(
    property_data: dict, param: str, pass_if_not_exist: bool = False
) -> ty.Optional[ty.Any]:
    is_param = param in property_data
    if pass_if_not_exist and not is_param:
        raise ValueError(f"{param} : must be in data keys")
    if not pass_if_not_exist and not is_param:
        return None
    return property_data[param]


def operate_rule_on_value(value, rule: Rule):
    try:
        vtype = type(value)
        rvalue = vtype(rule.value)  # evaluate the rule value to the same type
        operator = MAP_OPERATORS[rule.operator]
        return operator(value, rvalue)
    except Exception:
        msg = f"Cannot evaluate rule {rule} on value {value!r} of type {vtype!s}"
        logger.warning(msg)
        return False



def rule_check_category(category, rule: Rule):
    return category in rule.categories


def rule_check_dict(property_data: dict, rule: Rule, category=None) -> bool:
    if category is not None and not rule_check_category(category, rule):
        return False
    value = get_param_value(property_data, rule.parameter)
    if value is None:
        return False
    return operate_rule_on_value(value, rule)


def ruleset_check_dict(
    property_data: dict, rule_set: RuleSet, category: ty.Union[None, str] = None
) -> bool:
    li = [rule_check_dict(property_data, r, category=category) for r in rule_set.rule]
    if rule_set.set_type == RuleSetType.AND:
        return False not in li
    if rule_set.set_type == RuleSetType.OR:
        return True in li
    msg = "RuleSetType must be AND or OR"
    raise ValueError(msg)


def ruleset_check_dicts(
    li_property_data: list[dict],
    rule_set: RuleSet,
    li_categories: None | list = None,
) -> list[bool]:
    if li_categories is None:
        li_categories = [None] * len(li_property_data)
    elif len(li_categories) != len(li_property_data):
        msg = "len(li_categories) != len(li_property_data):"
        raise ValueError(msg)
    else:
        pass
    return [
        ruleset_check_dict(x, rule_set, category=li_categories[n])
        for n, x in enumerate(li_property_data)
    ]


# def operate_ruleset_on_value(value, rule_set: RuleSet):
#     li = [operate_rule_on_value(value, r) for r in rule_set.rules]
#     fn_or = lambda li: False if False in li else True
#     fn_and = lambda li: True if True in li else False

#     if rule_set.set_type == RuleSetType.AND:
#         return fn_and(li)
#     elif rule_set.set_type == RuleSetType.OR:
#         return fn_or(li)
#     else:
#         raise ValueError("RuleSetType must be AND or OR")