from pyrulefilter import filters
import subprocess
import doctest


def test_filters():
    doctest_results = doctest.testmod(m=filters)
    assert doctest_results.failed == 0
