import typing as ty
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator
from pyrulefilter.enums import (
    FilterCategoriesEnum,
    OperatorsEnum,
    RuleSetType,
)
from typing_extensions import Annotated


class BaseModel(BaseModel):  # https://github.com/pydantic/pydantic/issues/1836
    @classmethod
    def schema(cls, **kwargs):
        schema = super().schema(**kwargs)
        for fld_v in cls.__fields__.values():
            if fld_v.default_factory is not None:
                schema["properties"][fld_v.alias]["default"] = fld_v.default_factory()
        return schema


def html_link(url: str, description: str, color: str = "blue"):
    """returns an html link string to open in new tab

    Args:
        url (url):
        description (str): the text to display for the link
        color (str, optional): color of description text. Defaults to "blue".

    Returns:
        str: html text
    """
    return (
        f'<font color="{color}"><a href="{url}" target="blank"'
        f" >{description}</a></font>"
    )


URL_REVIT_FILTERS = "https://help.autodesk.com/view/RVT/2023/ENU/?guid=GUID-400FD74B-00E0-4573-B3AC-3965E65CBBDB"
URL_UNICLASS_SYSTEMS = "https://uniclass.thenbs.com/taxon/ss"
URL_UNICLASS_PRODUCTS = "https://uniclass.thenbs.com/taxon/pr"
HTMLLINK_UNICLASS_SYSTEMS = html_link(URL_UNICLASS_SYSTEMS, "Uniclass System codes 🔗")
HTMLLINK_UNICLASS_PRODUCTS = html_link(
    URL_UNICLASS_PRODUCTS, "Uniclass Product codes 🔗"
)


FilterCategories = Annotated[
    list[FilterCategoriesEnum], BeforeValidator(lambda v: [] if v is None else v)
]


class Rule(BaseModel):
    categories: FilterCategories = Field(
        default=[],
        title="Categories",  # TODO: this is pydantic bug (should generate title from field name)
        description="Revit MEP categories to filter by (i.e. revit object must belong to categories defined here). If empty, all categories are included.",
    )
    parameter: str = Field(
        description="name of schedule parameter against which to apply filter rule",
        json_schema_extra=dict(autoui="ipywidgets.Combobox"),
    )
    operator: OperatorsEnum = Field(
        title="Logical Operator",
        description="logical operator used to evaluate parameter value against value below",
    )
    value: str = Field(
        "",
        description="Value to filter by. Evaluates to the appropriate type. Leave empty if none required (e.g. has value operator)",
        json_schema_extra=dict(autoui="ipywidgets.Combobox"),
    )
    model_config = ConfigDict(
        json_schema_extra=dict(autoui="ipyautoui.demo_schemas.ruleset.rule_ui")
    )


RuleSet = ty.ForwardRef("RuleSet")


class RuleSet(BaseModel):
    set_type: RuleSetType = Field(default=RuleSetType.OR)
    rule: ty.List[ty.Union[Rule, RuleSet]] = Field(
        description="""
rules return a boolean for the logical evaluation defined below for every item within the categories defined
"""
    )

    model_config = ConfigDict(title="RuleSet")


RuleSet.__doc__ = (
    """A set of rules that defines what equipment specifications will appear in a given schedule.<br>
Rules must evaluate to True for the item to be included in a schedule.
This is analogous to how 
"""
    + html_link(URL_REVIT_FILTERS, "filter rules work in Revit.")
    + "<br>As such, rules defined are imported into Revit and are used to create Revit"
    " Schedules.<br><hr>"
)
