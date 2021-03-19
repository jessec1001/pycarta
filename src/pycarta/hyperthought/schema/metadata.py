from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Metadata"]


Link = class_generator(
    displayText=fields.Str(allow_none=True),
    link=fields.Field(allow_none=True),
    type=fields.Str(validate=validate.OneOf([
        "string",
        "link"
    ]))
)


Metadata = class_generator(
    keyName=fields.Str(),
    value=fields.Nested(Link.schema),
    annotation=fields.Str(allow_none=True, required=False),
    unit=fields.Str(allow_none=True, required=False),
    cdd_id=fields.Str(allow_none=True, required=False),
    cdd_name=fields.Str(allow_none=True, required=False)
)
