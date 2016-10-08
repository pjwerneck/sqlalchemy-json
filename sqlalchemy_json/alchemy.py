
import json

import sqlalchemy
from sqlalchemy.ext import mutable

from . import track


class NestedMutableDict(mutable.MutableDict, track.TrackedDict):
    """SQLAlchemy `mutable` extension dictionary with nested change tracking."""

    def __setitem__(self, key, value):
        """Ensure that items set are converted to change-tracking types."""
        super(NestedMutableDict, self).__setitem__(key, self.convert(value, self))

    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionary to NestedMutable."""
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super(cls).coerce(key, value)


class NestedMutableList(mutable.MutableList, track.TrackedList):
    """SQLAlchemy `mutable` extension list with nested change tracking."""

    def __setitem__(self, key, value):
        """Ensure that items set are converted to change-tracking types."""
        super(NestedMutableList, self).__setitem__(key, self.convert(value, self))

    @classmethod
    def coerce(cls, key, value):
        """Convert plain list to NestedMutableList."""
        if isinstance(value, cls):
            return value
        if isinstance(value, list):
            return cls(value)
        return super(cls).coerce(key, value)


class _JsonTypeDecorator(sqlalchemy.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = sqlalchemy.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class JsonObject(_JsonTypeDecorator):
    """JSON object type for SQLAlchemy with change tracking as base level."""


class NestedJsonDict(_JsonTypeDecorator):
    """JSON object type for SQLAlchemy with nested change tracking."""


class NestedJsonList(_JsonTypeDecorator):
    """JSON object type for SQLAlchemy with nested change tracking."""


mutable.MutableDict.associate_with(JsonObject)

NestedMutableDict.associate_with(NestedJsonDict)
NestedMutableList.associate_with(NestedJsonList)
