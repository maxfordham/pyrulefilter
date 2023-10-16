from pydantic import ConfigDict, BaseModel, Field
from pyrulefilter.enums import FilterCategoriesEnum, OperatorsEnum, RuleSetType
import typing as ty


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


class RuleBase(BaseModel):
    categories: ty.Optional[list[FilterCategoriesEnum]] = Field(
        default=None,
        title="Categories",  # TODO: this is pydantic bug (should generate title from field name)
        description=(
            "Revit MEP categories to filter by (i.e. object must belong to"
            " categories defined here). If empty, all categories are included."
        ),
        json_schema_extra=dict(column_width=120),
    )

    operator: OperatorsEnum = Field(
        description=(
            "logical operator used to evaluate parameter value against value below"
        ),
        json_schema_extra=dict(column_width=125),
    )
    value: str = Field(
        "",
        description=(
            "Value to filter by. Evaluates to the appropriate type. Leave empty if none"
            " required (e.g. has value operator)"
        ),
        json_schema_extra=dict(
            autoui="ipyautoui.autowidgets.Combobox", column_width=150
        ),
    )
    model_config = ConfigDict(
        allow_extra=True,
        json_schema_extra={
            "align_horizontal": False,
            "autoui": (
                "__main__.RuleUi"
            ),  # this explicitly defines RuleUi as the interface rather than AutoObject
        },
        from_attributes=True,
    )


class Rule(RuleBase):
    parameter: str = Field(
        description="name of schedule parameter against which to apply filter rule",
        json_schema_extra=dict(
            autoui="ipyautoui.autowidgets.Combobox", column_width=200
        ),
    )


uniclass_property_code_name = html_link(URL_UNICLASS_PRODUCTS, "UniclassPropertyCode 🔗")
uniclass_system_code_name = html_link(URL_UNICLASS_SYSTEMS, "UniclassSystemCode 🔗")
rules_des = f"""
each rule returns a boolean for the logical evaluation for every item from the requested categories.<br>
An example pattern is to:

<ul>
    <li>leave "Categories" blank, thus applying the rule to all items in all categories</li>
    <li>select {HTMLLINK_UNICLASS_PRODUCTS} / {HTMLLINK_UNICLASS_SYSTEMS} as the "Parameter"</li>
    <li>select "begins with" as the operator</li>
    <li>select the required code and subcode for "Value"</li>
</ul>
"""


class RuleSetBase(BaseModel):
    """defines a set of filter rules used to define what appears in a schedule"""

    name: str = Field(
        "",
        description="name of rule set. indicates schedule name in Revit",
        json_schema_extra=dict(column_width=200),
    )
    description: str = Field(
        "",
        description="optional description of rule set",
        json_schema_extra=dict(
            column_width=300, autoui="ipyautoui.autowidgets.Textarea"
        ),
    )
    set_type: RuleSetType = Field(
        default=RuleSetType.AND,
        description=(
            "OR/AND. OR(/AND) -> one(/all) rule(/s) must evaluate to True"
            " for the item to be included."
        ),
        json_schema_extra=dict(disabled=True, column_width=100),
    )
    model_config = ConfigDict(
        allow_extra=True, from_attributes=True, title="Rule Set Definition"
    )


class RuleSet(RuleSetBase):
    rules: list[Rule] = Field(
        description=rules_des,
        default_factory=lambda: [],
        json_schema_extra=dict(format="dataframe"),
    )
    model_config = ConfigDict(
        allow_extra=True,
        json_schema_extra={"align_horizontal": False},
        from_attributes=True,
    )


RuleSet.__doc__ = (
    """A set of rules that defines what equipment specifications will appear in a given schedule.<br>
Rules must evaluate to True for the item to be included in a schedule.
This is analogous to how 
"""
    + html_link(URL_REVIT_FILTERS, "filter rules work in Revit.")
    + "<br>As such, rules defined are imported into Revit and are used to create Revit"
    " Schedules.<br><hr>"
)
