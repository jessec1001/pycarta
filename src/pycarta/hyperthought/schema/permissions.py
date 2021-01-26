from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Permissions"]


Permissions = class_generator(
    projects=fields.Dict(
        keys=fields.Str(),
        values=fields.Str(allow_none=True),
        allow_none=True
    ),
    groups=fields.Dict(
        keys=fields.Str(),
        values=fields.Str(allow_none=True),
        allow_none=True
    ),
    users=fields.Dict(
        keys=fields.Str(),
        values=fields.Str(allow_none=True),
        allow_none=True
    )
)
