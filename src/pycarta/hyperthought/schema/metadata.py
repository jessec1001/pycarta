from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Metadata"]


Link = class_generator(
    type=fields.Str(validate=validate.OneOf([
        "string",
        "link"
    ])),
    link=fields.Field(allow_none=True)
)


Metadata = class_generator(
    keyName=fields.Str(),
    value=fields.Nested(Link.schema),
    annotation=fields.Str(allow_none=True, required=False),
    unit=fields.Str(allow_none=True, required=False),
    cdd_id=fields.Str(allow_none=True, required=False),
    cdd_name=fields.Str(allow_none=True, required=False)
)
