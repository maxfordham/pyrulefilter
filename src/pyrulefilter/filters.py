from __future__ import annotations

import logging
import operator
from pyrulefilter.enums import OperatorsEnum

logger = logging.getLogger(__name__)


def contains(a: str, b: str) -> bool:
    """Check a in b.

    Examples
    --------

        >>> contains("hello", "hell")
        True
        >>> contains("heel", "hello")
        False
    """
    return b in a


def not_contains(a: str, b: str) -> bool:
    """Check a not in b.

    Examples
    --------

        >>> not_contains("hello", "hell")
        False
        >>> not_contains("heel", "hello")
        True

    """
    return b not in a


def startswith(a: str, b: str) -> bool:
    """Check a startswith b.

    Examples
    --------

        >>> startswith("hello", "hell")
        True
        >>> startswith("heel", "hello")
        False

    """
    return bool(a.startswith(b))


def not_startswith(a: str, b: str) -> bool:
    """Check a not startswith b.

    Examples
    --------

        >>> not_startswith("hello", "hell")
        False
        >>> not_startswith("heel", "hello")
        True

    """
    return bool(not a.startswith(b))


def endswith(a: str, b: str) -> bool:
    """Check a endswith b.

    Examples
    --------

        >>> endswith("hello", "lo")
        True
        >>> endswith("hello", "elo")
        False

    """
    return bool(a.endswith(b))


def not_endswith(a: str, b: str) -> bool:
    """Check a not_endswith b.

    Examples
    --------

        >>> not_endswith("hello", "lo")
        False
        >>> not_endswith("hello", "elo")
        True

    """
    return bool(not a.endswith(b))


def isnone(a, b=None) -> bool:
    """Check a isnone.

    Examples
    --------

        >>> isnone("hello")
        False
        >>> isnone(None)
        True

    """
    return a is None


def not_isnone(a, b=None) -> bool:
    """Check a isnone.

    Examples
    --------

        >>> not_isnone("hello")
        True
        >>> not_isnone(None)
        False

    """
    return a is not None


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


