import pytest
from ascs import params


def test_check_la_codes_are_consistent(monkeypatch):
    monkeypatch.setattr(params, "ALL_LA_CODES", [211, 212])
    monkeypatch.setattr(params, "STRATIFIED_BY_LA_CORRECT_ROW_ORDER", [211, 213])  #

    with pytest.raises(AssertionError) as err:
        params.check_la_codes_are_consistent()

    assert "212" in str(err.value)
