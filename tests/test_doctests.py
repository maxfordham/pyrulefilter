from pyrulefilter import filters
import subprocess

CMD = "pytest --doctest-modules"


def test_filters():
    complete = subprocess.call(f"{CMD} {filters.__file__}", shell=True)
    assert complete == 0
