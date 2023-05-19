from pydantic import BaseModel, Field
from pyrulefilter.enums import FilterCategoriesEnum, OperatorsEnum, RuleSetType


class BaseModel(BaseModel):  # https://github.com/pydantic/pydantic/issues/1836
    @classmethod
    def schema(cls):
        schema = super().schema()
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


class Rule(BaseModel):
    categories: list[FilterCategoriesEnum] = Field(
        default_factory=lambda: [],
        title="Categories",  # TODO: this is pydantic bug (should generate title from field name)
        description=(
            "Revit MEP categories to filter by (i.e. object must belong to"
            " categories defined here). If empty, all categories are included."
        ),
    )
    parameter: str = Field(
        description="name of schedule parameter against which to apply filter rule",
        autoui="ipyautoui.autowidgets.Combobox",
    )
    operator: OperatorsEnum = Field(
        description=(
            "logical operator used to evaluate parameter value against value below"
        )
    )
    value: str = Field(
        "",
        description=(
            "Value to filter by. Evaluates to the appropriate type. Leave empty if none"
            " required (e.g. has value operator)"
        ),
        autoui="ipyautoui.autowidgets.Combobox",
    )

    class Config:
        allow_extra = True
        schema_extra = {
            "align_horizontal": False,
            "autoui": "__main__.RuleUi",  # this explicitly defines RuleUi as the interface rather than AutoObject
        }
        orm_mode = True


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


class RuleSet(BaseModel):
    set_type: RuleSetType = Field(default=RuleSetType.AND, disabled=True)
    rules: list[Rule] = Field(description=rules_des)
    name: str = Field(
        None, description="name of rule set. indicates schedule name in Revit"
    )

    # NOTE: in future maybe make rules recursive (like Revit)
    # i.e.
    # rules: list[ty.Union[Rule, RuleSet]]

    class Config:
        allow_extra = True
        schema_extra = {"align_horizontal": False}
        orm_mode = True


RuleSet.__doc__ = (
    """A set of rules that defines what equipment specifications will appear in a given schedule.<br>
Rules must evaluate to True for the item to be included in a schedule.
This is analogous to how 
"""
    + html_link(URL_REVIT_FILTERS, "filter rules work in Revit.")
    + "<br>As such, rules defined are imported into Revit and are used to create Revit"
    " Schedules.<br><hr>"
)
