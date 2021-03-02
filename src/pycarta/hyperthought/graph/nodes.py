from ...base import Node
from ..schema import File, Workflow, WorkflowTemplate
from copy import deepcopy

import logging
logger = logging.getLogger(__name__)


class HyperthoughtNode(Node):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def __hash__(self):
        return super().__hash__()

    # Accessors to properties defined in the Hyperthought schema
    @property
    def name(self):
        if isinstance(self.contents, (File, Workflow)):
            return self.contents["content"]["name"]
        elif isinstance(self.contents, WorkflowTemplate):
            return self.contents["name"]
        else:
            return getattr(super(), "name", self.key)

    @name.setter
    def name(self, value):
        if isinstance(self.contents, (File, Workflow)):
            self.contents["content"]["name"] = value
        elif isinstance(self.contents, WorkflowTemplate):
            self.contents["name"] = value
        else:
            super().name = value

    @property
    def key(self):
        if isinstance(self.contents, (File, Workflow)):
            return self.contents["content"]["pk"]
        elif isinstance(self.contents, WorkflowTemplate):
            return self.contents["key"]
        else:
            return None
