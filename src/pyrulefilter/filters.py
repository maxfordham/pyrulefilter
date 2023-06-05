import typing as ty
from pyrulefilter.schemas import Rule, RuleSet, RuleSetType
from pyrulefilter.enums import OperatorsEnum  # FilterCategoriesEnum,
import operator
import logging

logger = logging.getLogger(__name__)

# from aectemplater_schemas.type_spec import TypeSpecification


def contains(a: str, b: str) -> bool:
    """check a in b

    Example:
        >>> contains("hello", "hell")
        True
        >>> contains("heel", "hello")
        False
    """
    if b in a:
        return True
    else:
        return False


def not_contains(a: str, b: str) -> bool:
    """check a not in b

    Example:
        >>> not_contains("hello", "hell")
        False
        >>> not_contains("heel", "hello")
        True
    """
    if b not in a:
        return True
    else:
        return False


def startswith(a: str, b: str) -> bool:
    """check a startswith b

    Example:
        >>> startswith("hello", "hell")
        True
        >>> startswith("heel", "hello")
        False
    """
    if a.startswith(b):
        return True
    else:
        return False


def not_startswith(a: str, b: str) -> bool:
    """check a not startswith b

    Example:
        >>> not_startswith("hello", "hell")
        False
        >>> not_startswith("heel", "hello")
        True
    """
    if not a.startswith(b):
        return True
    else:
        return False  #


def endswith(a: str, b: str) -> bool:
    """check a endswith b

    Example:
        >>> endswith("hello", "lo")
        True
        >>> endswith("hello", "elo")
        False
    """
    if a.endswith(b):
        return True
    else:
        return False


def not_endswith(a: str, b: str) -> bool:
    """check a not_endswith b

    Example:
        >>> not_endswith("hello", "lo")
        False
        >>> not_endswith("hello", "elo")
        True
    """
    if not a.endswith(b):
        return True
    else:
        return False


def isnone(a, b=None) -> bool:
    """check a isnone

    Example:
        >>> isnone("hello")
        False
        >>> isnone(None)
        True
    """
    if a is None:
        return True
    else:
        return False


def not_isnone(a, b=None) -> bool:
    """check a isnone

    Example:
        >>> not_isnone("hello")
        True
        >>> not_isnone(None)
        False
    """
    if a is not None:
        return True
    else:
        return False


MAP_OPERATORS = {
    # OperatorsEnum.Less: operator.lt,
    # OperatorsEnum.LessOrEqual: operator.le,
    OperatorsEnum.Equals: operator.eq,
    OperatorsEnum.NotEquals: operator.ne,
    # OperatorsEnum.GreaterOrEqual: operator.ge,
    # OperatorsEnum.Greater: operator.gt,
    OperatorsEnum.Contains: contains,
    OperatorsEnum.NotContains: not_contains,
    OperatorsEnum.BeginsWith: startswith,
    OperatorsEnum.NotBeginsWith: not_startswith,
    OperatorsEnum.EndsWith: endswith,
    OperatorsEnum.NotEndsWith: not_endswith,
    # OperatorsEnum.HasValueParameter: isnone,
    # OperatorsEnum.HasNoValueParameter: not_isnone,
}

# "CreateIsAssociatedWithGlobalParameterRule": "?",
# "CreateIsNotAssociatedWithGlobalParameterRule": "?",
# "CreateSharedParameterApplicableRule": "?"
# ^^^ revit filters not mapped...


def get_param_value(
    property_data: dict, param: str, pass_if_not_exist: bool = False
) -> ty.Optional[ty.Any]:
    is_param = param in property_data.keys()
    if pass_if_not_exist and not is_param:
        raise ValueError(f"{param} : must be in data keys")
    elif not pass_if_not_exist and not is_param:
        return None
    else:
        return property_data[param]


def operate_rule_on_value(value, rule: Rule):
    try:
        vtype = type(value)
        rvalue = vtype(rule.value)  # evaluate the rule value to the same type
        operator = MAP_OPERATORS[rule.operator]
        return operator(value, rvalue)
    except:
        logger.warning(
            f"rule.value={str(rule.value)} cannot be evaluated to {str(vtype)}"
        )
        return False


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


def rule_check_category(category, rule: Rule):
    if category in rule.categories:
        return True
    else:
        return False


def rule_check_dict(property_data: dict, rule: Rule, category=None) -> bool:
    if category is not None:
        if not rule_check_category(category, rule):
            return False
    value = get_param_value(property_data, rule.property)
    if value is None:
        return False
    else:
        return operate_rule_on_value(value, rule)


def ruleset_check_dict(
    property_data: dict, rule_set: RuleSet, category: ty.Union[None, str] = None
) -> bool:
    li = [rule_check_dict(property_data, r, category=category) for r in rule_set.rules]
    fn_and = lambda li: False if False in li else True
    fn_or = lambda li: True if True in li else False

    if rule_set.set_type == RuleSetType.AND:
        return fn_and(li)
    elif rule_set.set_type == RuleSetType.OR:
        return fn_or(li)
    else:
        raise ValueError("RuleSetType must be AND or OR")


def ruleset_check_dicts(
    li_property_data: list[dict],
    rule_set: RuleSet,
    li_categories: ty.Union[None, list] = None,
) -> list[bool]:
    if li_categories is None:
        li_categories = [None] * len(li_property_data)
    elif len(li_categories) != len(li_property_data):
        raise ValueError("len(li_categories) != len(li_property_data):")
    else:
        pass
    return [
        ruleset_check_dict(l, rule_set, category=li_categories[n])
        for n, l in enumerate(li_property_data)
    ]


# def check_type_spec(psetspec: TypeSpecification, rule: Rule):
#     return rule_check_dict(psetspec.property_data, rule)


# UDATA = UnitsBaseData()
# MAP_TYPES = UDATA.map_schema_types

# def map_types(di):
#     _map = di["ifc_data_type"]  # (di['Property Value Kind'], di['Ifc Data Type'])
#     try:
#         return di | MAP_TYPES[_map]
#     except:
#         return di | {"type": "string"}
