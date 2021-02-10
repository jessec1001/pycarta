import pytest
import json
from pycarta import hyperthought as ht
from marshmallow import fields, validate, ValidationError


def raises_error(func, error_type):
    try:
        func()
        assert False, f"Should raise {error_type.__name__}."
    except error_type:
        pass


@pytest.fixture
def load_file():
    with open("resources/hyperthought_20210210.json") as ifs:
        return json.load(ifs)


class TestLoad:
    def test_valid(self, load_file):
        obj = ht.schema.load(load_file)

    def test_invalid(self, load_file):
        data = load_file
        # invalid value
        data["content"]["pk"] = ""
        raises_error(lambda: ht.schema.load(data), ValueError)
        # required parameter missing
        del data["content"]["pk"]
        raises_error(lambda: ht.schema.load(data, strict=True), ValueError)
        # force ignores all invalid data.
        obj = ht.schema.load(data, force=True)
