import re
import json
import marshmallow as mm
import pandas as pd
from typing import Optional, Callable
from collections.abc import MutableMapping


__all__ = ["class_generator"]


def class_generator(**schema):
    class Container(MutableMapping):
        schema = None

        def __init__(self, **kwds):
            """
            Object to hold data defined by the schema defined by the
            enclosing generator.

            Attributes
            ----------
            schema : marshmallow.Schema
                Schema definition for this class.

            Methods
            -------
            class.load(data)
                Loads JSON-serialized data.

            class.loads(data)
                Loads JSON-serialized data from a string.

            instance.dump()
                Return a formatted result of the object.

            instance.dumps()
                Returns a string-formatted result of the object.
            """
            self.__dict__.update(kwds)
            self.__keys = set(kwds.keys())

        def __getitem__(self, key):
            return self.__dict__[key]

        def __setitem__(self, key, value):
            self.__dict__[key] = value
            self.__keys.add(key)

        def __delitem__(self, key):
            self.__dict__[key]
            self.__keys -= set((key,))

        def __iter__(self):
            return iter(self.__keys)

        def __len__(self):
            return len(self.__keys)

        @staticmethod
        def load(data, **kwds):
            kwds['many'] = True if isinstance(data, list) else False
            schema = Container.schema(**kwds)
            for field in schema.fields.values():
                if hasattr(field, 'unknown'):
                    # field.unknown = kwds.get('unknown', None)
                    field.unknown = kwds.get('unknown', field.unknown)
            return schema.load(data)

        @staticmethod
        def loads(data, **kwds):
            return Container.load(json.loads(data), **kwds)

        def dump(self):
            return Container.schema().dump(self)

        def dumps(self):
            return Container.schema().dumps(self)


    # construct the schema and assign to the newly-created class.
    def propagate_unknown(self, data, **kwds):
        for field in self.fields.values():
            if hasattr(field, 'unknown'):
                # field.unknown = self.unknown
                field.unknown = getattr(self, "unknown", field.unknown)
        return data
    def empty_string_to_null(self, data, **kwds):
        return {k:(v or None) for k,v in data.items()}
    def create(self, data, **kwds):
        return Container(**data)
    ContainerSchema = type(
        "ContainerSchema",
        (mm.Schema,),
        dict(
            **schema,
            set_unknown=mm.pre_load(propagate_unknown),
            nullstr=mm.pre_load(empty_string_to_null),
            create=mm.post_load(create)
        )
    )
    setattr(Container, "schema", ContainerSchema)

    return Container
