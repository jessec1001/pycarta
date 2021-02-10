from ...base import class_generator
from .header import Header
from .metadata import Metadata
from .permissions import Permissions
from .restrictions import Restrictions
from .triples import Triple
from marshmallow import fields, validate


__all__ = ["FileContent", "File"]


FileContent = class_generator(
    backend=fields.Str(
        validate=validate.OneOf([
            "default",
            "s3"
        ])
    ),
    created=fields.DateTime(),
    created_by=fields.Str(),
    file=fields.UUID(allow_none=True),
    ftype=fields.Str(allow_none=True),
    items=fields.Int(allow_none=True),
    modified=fields.DateTime(allow_none=True),
    modified_by=fields.Str(allow_none=True),
    name=fields.Str(),
    path=fields.Str(
        validate=validate.Regexp(
            r'^,((urn:uuid:)?\w{8}-\w{4}-\w{4}-\w{4}-\w{12},)*$'
        ),
        allow_none=True
    ),
    path_string=fields.Str(allow_none=True),
    pk=fields.UUID(),
    size=fields.Int(allow_none=True)
)


File = class_generator(
    content=fields.Nested(FileContent.schema),
    triples=fields.List(
        fields.Nested(Triple.schema),
        allow_none=True),
    metadata=fields.List(
        fields.Nested(Metadata.schema),
        allow_none=True),
    header=fields.Nested(Header.schema),
    permissions=fields.Nested(Permissions.schema),
    restrictions=fields.Nested(Restrictions.schema)
)
