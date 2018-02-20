import pytest

from flask_dialogflow.helpers import TypedList


class TestTypedList:
    def test_type(self):
        class Dummy:
            pass
        obj = TypedList(Dummy)
        assert isinstance(Dummy(), obj.type)

    def test_empty(self):
        obj = TypedList(str)
        assert len(obj) == 0, "the list is non empty"

    def test_exception(self):
        class Dummy:
            pass
        with pytest.raises(Exception) as excinfo:
            obj = TypedList(Dummy)
            obj.append(1)   
        assert 'item is not of type' in str(excinfo.value)

    def test_append(self):
        obj = TypedList(int)
        obj.append(1)
        assert len(obj) == 1
        assert obj[0] == 1
        obj.append(2)
        assert obj[1] == 2