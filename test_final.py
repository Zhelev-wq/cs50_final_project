import pytest
from final_project import get_keywords

def test_get_keywords(mocker):
    mocker.patch('builtins.input', side_effect=["online casino", "casino online", "casino site"])
    test = get_keywords(3)
    assert test == [{'keyword': 'online casino', 'number':0}, {'keyword':'casino online', 'number':0}, {'keyword':'casino site', 'number':0}]

