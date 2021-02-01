from ...base import class_generator
from marshmallow import fields, validate


__all__ = ["Restrictions"]


Restrictions = class_generator(
    distribution = fields.String(
        validate=lambda check: check.lower() in [
            "distribution a",
            "distribution b",
            "distribution c",
            "distribution d",
            "distribution e",
            "distribution f"
        ],
        allow_none=True
    ),
    exportControl = fields.String(
        validate=validate.OneOf([
            "itar",
            "ear"
        ]),
        allow_none=True
    ),
    securityMarking = fields.String(allow_none=True)
)
