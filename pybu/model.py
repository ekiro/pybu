from pybu.fields import Field


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        fields = set()
        for field, value in attrs.items():
            if isinstance(value, Field):
                fields.add(field)
                value._field_name = field
        cls._fields = frozenset(fields)
        return cls


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        ret = {}
        for field in self._fields:
            ret[field] = getattr(self, field)

        return ret

    def __eq__(self, other):
        return all(getattr(self, f) == getattr(other, f) for f in self._fields)
