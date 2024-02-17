# test/conftest.py

import pytest


@pytest.fixture(scope="session")
def data_file(tmp_path_factory):
    data = "career;hd;sd\n"
    data += "fighter;1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;\n"
    data += (
        "mage;1,1,2,2,3,3,4,4,5,5,6,6,7,7,8;0,1,1,2,2,3,3,4,4,5,5,6,6,7,7\n"
    )
    data += (
        "cleric;1,1,2,3,3,4,5,5,6,7,7,8,9,9,10;0,1,1,1,2,2,2,3,3,3,4,4,4,5,5\n"
    )
    fn = tmp_path_factory.mktemp("data") / "levels.txt"
    with open(fn, "w") as f:
        f.write(data)
    return fn
