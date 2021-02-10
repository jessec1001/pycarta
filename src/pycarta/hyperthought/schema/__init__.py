from .file import *
from .header import *
from .metadata import *
from .permissions import *
from .restrictions import *
from .triples import *
from .workflow import *


class LoadWarning(Warning):
    pass


def load(contents, force: bool=False, strict: bool=False):
    """
    Attempts to load HyperThought formatted data based on all known
    HyperThought schema.

    Parameters
    ==========
    contents : dict
        Contents to be parsed.
    force : bool
        Read all valid data.
    strict : bool
        If True, then only data that matches a known schema element will be
        read. If False, the default, then missing and unknown fields will be
        read, even if the schema requires them.

    Returns
    =======
        HyperThought schema object populated with the data from `contents`.
    """
    from marshmallow import ValidationError
    import marshmallow as mm
    import warnings

    def similarity(err):
        """Qualitative similarlity metric"""
        def count(d, pattern=None, **kwds):
            import re
            if isinstance(d, str) and pattern is not None:
                return (1 if re.match(pattern, d, **kwds) else 0)
            elif isinstance(d, dict):
                return sum([count(v, pattern, **kwds) for v in d.values()])
            elif isinstance(d, (list, tuple, set)):
                return sum([count(x, pattern, **kwds) for x in d])
            else:
                if pattern is not None:
                    raise ValueError(f"{type(d)} is not a recognized type.")
                else:
                    return 1

        unknown = count(err.messages, "^Unknown field")
        invalid = count(err.messages, "^Not a valid")
        missing = count(err.messages, "^Missing data")
        valid = count(err.valid_data)
        read = count(err.data)

        return valid/read

    quality = dict()
    try:
        return File.load(contents)
    except ValidationError as e:
        quality[File] = similarity(e)
    try:
        return FileContent.load(contents)
    except ValidationError as e:
        quality[FileContent] = similarity(e)
    try:
        return Header.load(contents)
    except ValidationError as e:
        quality[Header] = similarity(e)
    try:
        return Metadata.load(contents)
    except ValidationError as e:
        quality[Metadata] = similarity(e)
    try:
        return Permissions.load(contents)
    except ValidationError as e:
        quality[Permissions] = similarity(e)
    try:
        return Restrictions.load(contents)
    except ValidationError as e:
        quality[Restrictions] = similarity(e)
    try:
        return Triple.load(contents)
    except ValidationError as e:
        quality[Triple] = similarity(e)
    try:
        return WorkflowTemplate.load(contents)
    except ValidationError as e:
        quality[WorkflowTemplate] = similarity(e)
    try:
        return Workflow.load(contents)
    except ValidationError as e:
        quality[Workflow] = similarity(e)
    try:
        return WorkflowContent.load(contents)
    except ValidationError as e:
        quality[WorkflowContent] = similarity(e)

    # if we get here, then none of the schemas are a perfect fit.
    best = {v:k for k,v in quality.items()}[max(quality.values())]
    message = f"No valid Hyperthought schema was found. " \
              f"{best.__name__}, with a similarity score of " \
              f"{max(quality.values())}, may be adapted " \
              f"to accept missing and extra values."
    if strict:
        raise ValueError(message)
    else:
        warnings.warn(message, LoadWarning)

    try:
        # try to read the best allowing for missing data, loosing requirements
        # and including extra data not defined in the schema.
        return best.load(
            contents,
            partial=True,  # handle missing fields
            unknown=mm.INCLUDE)
    except ValidationError as e:
        # still fails, indicating a more complex deviation from the schema
        from pprint import pformat
        if force:
            # force processes only the valid data
            warnings.warn(f"The following data will be lost during force: "
                         f"{pformat(e.messages)}")
            return load(e.valid_data, force=force)
        else:
            # otherwise, the load fails with a Value Error.
            raise ValueError(f"Could not read modified {best.__name__}. "
                             f"Error:\n{pformat(e.__dict__)}\n")


def loads(contents):
    import json
    return load(json.loads(contents))
