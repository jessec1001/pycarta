from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Triple"]


Value = class_generator(
    value=fields.Str(allow_none=True)
)


Triple = class_generator(
    subject=fields.Nested(Value.schema),
    predicate=fields.Nested(Value.schema),
    object=fields.Nested(Value.schema)
)
