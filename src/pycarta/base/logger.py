import inspect
import logging
import types

from functools import wraps


def functionlogger(fn):
    function_name = fn.__name__
    logger = logging.getLogger(name)
    @wraps(fn)
    def wrapper(*args, **kwds):
        state = "Success"
        try:
            result = fn(*args, **kwargs)
        except:
            state = "Failed"
            raise
        else:
            return result
        finally:
            logger.debug("%s (%s)", function_name, state)
    return wrapper


class MetaLogger(type):
    """
    Metaclass to enable automatic logging for every function that
    uses MetaLogger as a metaclass.
    """
    def __new__(cls, name, base, dct):
        _type = super().__new__(cls, name, base, dct)
        _type.logger = logging.getLogger(name)
        _type.logger.setLevel(logging.DEBUG)
        MetaLogger.update_class_methods(_type)
        return _type

    @staticmethod
    def add_log_decorator(cls, attribute, attribute_name):
        """
        Decoration function which is used for logging the success
        or failure of every function.
        """
        @wraps(attribute)
        def wrapper(*args, **kwargs):
            logger = cls.logger
            state = "Success"
            try:
                result = attribute(*args, **kwargs)
            except:
                state = "Failed"
                raise
            else:
                return result
            finally:
                logger.debug("%s (%s)", attribute_name, state)
        return wrapper

    @staticmethod
    def update_class_methods(cls):
        """
        Updates each class to ensure it is has been wrapped to log events.
        """
        if not hasattr(cls, "__decorated"):
            for attr_name, attr in inspect.getmembers(cls):
                if isinstance(attr, types.FunctionType):
                    setattr(
                        cls,
                        attr_name,
                        MetaLogger.add_log_decorator(
                            cls,
                            attr,
                            cls.__name__ + '.' + attr_name
                        )
                    )
        cls.__decorated = True
