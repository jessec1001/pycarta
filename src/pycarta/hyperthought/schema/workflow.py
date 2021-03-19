from ...base import class_generator
from .header import Header
from .metadata import Metadata
from .permissions import Permissions
from .restrictions import Restrictions
from .triples import Triple
from marshmallow import fields, validate


__all__ = ["WorkflowContent", "Workflow", "WorkflowTemplate"]


Hyperthought = class_generator(
    name=fields.Str(allow_none=True),
    objectType=fields.Str(allow_none=True)
)


WorkflowContent = class_generator(
    assignee=fields.Str(allow_none=True),
    children=fields.List(fields.UUID(), allow_none=True),
    client_id=fields.UUID(allow_none=True),
    completed=fields.DateTime(allow_none=True),
    created=fields.DateTime(),
    creator=fields.Str(),
    modified=fields.DateTime(allow_none=True),
    modifier=fields.Str(allow_none=True),
    name=fields.Str(),
    notes=fields.Str(allow_none=True),
    parent_process=fields.UUID(allow_none=True),
    pid=fields.UUID(allow_none=True),
    pk=fields.UUID(required=True),
    predecessors=fields.List(fields.UUID(), allow_none=True),
    process_type=fields.Str(
        validate=validate.OneOf([
            "workflow",
            "decision",
            "process"
        ])
    ),
    started=fields.DateTime(allow_none=True),
    status=fields.Str(
        validate=validate.OneOf([
            'pending',
            'in progress',
            'awaiting assignee',
            'manager review',
            'rejected',
            'completed',
            'workflow complete',
            'will not execute'
        ]),
        allow_none=True
    ),
    successors=fields.List(fields.UUID(), allow_none=True),
    template=fields.Boolean(),
    xml=fields.Str(allow_none=True)

)


Workflow = class_generator(
    content=fields.Nested(WorkflowContent.schema),
    triples=fields.List(
        fields.Nested(Triple.schema),
        allow_none=True
    ),
    metadata=fields.List(
        fields.Nested(Metadata.schema),
        allow_none=True
    ),
    headers=fields.Nested(Header.schema),
    hyperthought=fields.Nested(Hyperthought.schema),
    permissions=fields.Nested(Permissions.schema),
    restrictions=fields.Nested(Restrictions.schema)
)


WorkflowTemplate = class_generator(
    createdBy=fields.Str(),
    createdByFullName=fields.Str(),
    createdOn=fields.DateTime(),
    icon=fields.Str(allow_none=True),
    key=fields.UUID(),
    lazy=fields.Boolean(allow_none=True),
    modifiedBy=fields.Str(allow_none=True),
    modifiedByFullName=fields.Str(allow_none=True),
    modifiedOn=fields.DateTime(allow_none=True),
    name=fields.Str(),
    title=fields.Str()
)
