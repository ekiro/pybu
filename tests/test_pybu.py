import pytest

import pybu
from pybu.exceptions import FieldTypeError


@pytest.fixture
def model1():
    class Model1(pybu.Model):
        string = pybu.Str()
        integer = pybu.Int()
        boolean = pybu.Bool()
        flt = pybu.Float(required=False)

    return Model1


@pytest.fixture
def model2():
    class Model2(pybu.Model):
        elements = pybu.Tuple(type_=int)

    return Model2


@pytest.fixture
def model3(model1):
    class Model3(pybu.Model):
        objects = pybu.Tuple(type_=model1)
        elements = pybu.Tuple()

    return Model3


def test_base_functions(model1):
    obj = model1(string='test', integer=1, boolean=True, flt=5.0)

    assert obj.string == 'test'
    assert obj.integer == 1
    assert obj.boolean == True
    assert obj.flt == 5.0

    assert obj.to_dict() == dict(
        string='test', integer=1, boolean=True, flt=5.0)

    obj.string = 'test2'
    assert obj.string == 'test2'

    with pytest.raises(FieldTypeError):
        obj.string = True

    with pytest.raises(FieldTypeError):
        model1(integer="not int", string='str', boolean=False)

    obj2 = model1(**obj.to_dict())

    for field in model1._fields:
        assert getattr(obj, field) == getattr(obj2, field)

    assert obj == obj2
    assert obj is not obj2


def test_tuple_type(model2):
    obj = model2(elements=(1, 2, 3))

    assert obj.elements == (1, 2, 3)

    with pytest.raises(FieldTypeError):
        obj.elements = (1, 2, 'a')

    with pytest.raises(FieldTypeError):
        model2(elements=(1, 2, 'a'))


def test_serialization(model1, model3):
    obj1_1 = model1(string='test', integer=1, boolean=True, flt=5.0)
    obj1_2 = model1(string='test', integer=2, boolean=True, flt=5.0)

    obj3 = model3(objects=(obj1_1, obj1_2), elements=(obj1_1, 1, "x"))

    assert obj3.to_dict() == {
        'elements': [
            {'boolean': True, 'flt': 5.0, 'integer': 1, 'string': 'test'},
            1, 'x'],
        'objects': [
            {'boolean': True, 'flt': 5.0, 'integer': 1, 'string': 'test'},
            {'boolean': True, 'flt': 5.0, 'integer': 2, 'string': 'test'}
        ]}
