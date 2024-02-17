# test/test_career_info.py

import pytest
import write_char


def test_passing():
    assert 1 == 1


def test_data_file(data_file):
    with open(data_file, "r") as df:
        data = df.read()
    assert "fighter" in data


def test_ci(data_file, capsys):
    ci = write_char.CareerInfoBuilder(data_file).build()
    assert ci.get_info("fighter", 3) == (4, 0)
    assert ci.get_info("Cleric", 2) == (2, 1)


def test_ci_sysexit(data_file, capsys):
    ci = write_char.CareerInfoBuilder(data_file).build()
    with pytest.raises(SystemExit) as wrapped_e:
        ci.get_info("druid", 2)
    assert wrapped_e.type == SystemExit
    captured = capsys.readouterr()
    assert "established" in captured.out
