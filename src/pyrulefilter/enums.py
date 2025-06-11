from enum import Enum
import csv
import pathlib
import os

if "PATH_PYRULEFILTER_CATEGORIES" in os.environ:
    PATH_PYRULEFILTER_CATEGORIES = pathlib.Path(
        os.environ["PATH_PYRULEFILTER_CATEGORIES"]
    )
else:
    PATH_PYRULEFILTER_CATEGORIES = pathlib.Path(__file__).parent / "categories.csv"


def read_csv(p: pathlib.Path):
    # NOTE: could use pandas for this but it is heavy so could slow imports down.
    li = list(csv.reader(p.read_text().split("\n"), delimiter=","))
    return [dict(zip(li[0], li[n])) for n in range(1, len(li)) if li[n] != []]


def get_categories(filter=True):
    li = read_csv(PATH_PYRULEFILTER_CATEGORIES)
    if filter:
        li = [x for x in li if bool(int(x["Include"]))]
    return {x["Category"]: x["Name"] for x in li}


class OperatorsEnum(str, Enum):
    BeginsWith = "begins with"
    Contains = "contains"
    EndsWith = "ends with"
    Equals = "equals"
    # GreaterOrEqual = "is greater than or equal to"
    # Greater = "is greater than"
    # HasNoValueParameter = "has no value"
    # HasValueParameter = "has value"
    # IsAssociatedWithGlobalParameterRule = "?"
    # IsNotAssociatedWithGlobalParameterRule = "?"
    # LessOrEqual = "is less than or equal to"
    # Less = "is less than"
    NotBeginsWith = "does not begin with"
    NotContains = "does not contain"
    NotEndsWith = "does not end with"
    NotEquals = "does not equal"
    # SharedParameterApplicableRule = "?"


class StrEnum(str, Enum):
    pass


FilterCategoriesEnum = StrEnum("FilterCategoriesEnum", get_categories())


class RuleSetType(str, Enum):
    AND = "AND"
    OR = "OR"


