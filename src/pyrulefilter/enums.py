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
        li = [l for l in li if bool(int(l["Include"]))]
    return {l["Category"]: l["Name"] for l in li}


class OperatorsEnum(str, Enum):
    BeginsWith = "begins with"
    Contains = "contains"
    EndsWith = "ends with"
    Equals = "equals"
    GreaterOrEqual = "is greater than or equal to"
    Greater = "is greater than"
    HasNoValueParameter = "has no value"
    HasValueParameter = "has value"
    # IsAssociatedWithGlobalParameterRule = "?"
    # IsNotAssociatedWithGlobalParameterRule = "?"
    LessOrEqual = "is less than or equal to"
    Less = "is less than"
    NotBeginsWith = "does not begin with"
    NotContains = "does not contain"
    NotEndsWith = "does not end with"
    NotEquals = "dont not equal"
    # SharedParameterApplicableRule = "?"


class StrEnum(str, Enum):
    pass


CategoriesEnum = StrEnum("CategoriesEnum", get_categories())

class RuleSetType(str, Enum):
    AND = "AND"
    OR = "OR"

# REF
# {
#     "revit_version": "2022",
#     "revit_version_name": "Autodesk Revit 2022",
#     "revit_api_query": "Autodesk.Revit.DB.ParameterFilterRuleFactory",
#     "revit_api_docs": "https://www.revitapidocs.com/2023/317755a4-24ba-9f36-7639-f6fb2aa5a1a7.htm",
#     "data": {
#         "CreateBeginsWithRule": "begins with",
#         "CreateContainsRule": "contains",
#         "CreateEndsWithRule": "ends with",
#         "CreateEqualsRule": "equals",
#         "CreateGreaterOrEqualRule": "is greater than or equal to",
#         "CreateGreaterRule": "is greater than",
#         "CreateHasNoValueParameterRule": "has no value",
#         "CreateHasValueParameterRule": "has value",
#         "CreateIsAssociatedWithGlobalParameterRule": "?",
#         "CreateIsNotAssociatedWithGlobalParameterRule": "?",
#         "CreateLessOrEqualRule": "is less than or equal to",
#         "CreateLessRule": "is less than",
#         "CreateNotBeginsWithRule": "does not begin with",
#         "CreateNotContainsRule": "does not contain",
#         "CreateNotEndsWithRule": "does not end with",
#         "CreateNotEqualsRule": "dont not equal",
#         "CreateSharedParameterApplicableRule": "?"
#     }
# }
