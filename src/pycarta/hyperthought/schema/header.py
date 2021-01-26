from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Header"]


Header = class_generator(
    canonincal_uri=fields.Str(
        data_key="canonical-uri",
        allow_none=True
    ),
    sys_creation_timestamp=fields.DateTime(
        data_key="sys-creation-timestamp"
    ),
    sys_last_modified=fields.DateTime(
        data_key="sys-last-modified",
        allow_none=True
    ),
    createdBy=fields.Str(),
    modifiedBy=fields.Str(allow_none=True),
    uri=fields.Str(allow_none=True),  # Should this be URL?
    pid=fields.UUID(allow_none=True)
)
