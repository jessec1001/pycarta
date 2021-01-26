import pytest
import json
from marshmallow import fields, validate, ValidationError
from pycarta.base import class_generator


class TestBase:
    def test_datetime(self):
        import datetime as dt

        good_data = {
            'birthday': '1978-04-01T19:36+08:00'
        }
        bad_data = {
            'birthday': 'April 1, 1978'
        }
        Bday = class_generator(
            birthday=fields.DateTime()
        )
        good = Bday.load(good_data)
        assert good.birthday == dt.datetime.fromisoformat(good_data["birthday"])
        try:
            bad = Bday.load(bad_data)
        except ValidationError:
            pass

    def test_email(self):
        pass

    def test_string(self):
        data = {
            'title': 'Hello, World'
        }
        # good
        Good = class_generator(
            title=fields.Str()
        )
        good = Good.load(data)
        assert good.title == data['title']
        good = Good.loads(json.dumps(data))
        assert good.title == data['title']
        assert json.loads(good.dumps()) == data
        # bad
        Bad = class_generator(
            name=fields.Str()
        )
        try:
            bad = Bad.load(data)
        except ValidationError:
            pass
        try:
            bad = Bad.loads(json.dumps(data))
        except ValidationError:
            pass

    def test_enum(self):
        good_data = {
            'select': 'foo'
        }
        bad_data = {
            'select': 'foobar'
        }
        enum = class_generator(
            select=fields.Str(validate=validate.OneOf([
                'foo', 'bar', 'baz'
            ]))
        )
        good = enum.load(good_data)
        assert good.select == good_data['select']
        try:
            bad = enum.load(bad_data)
        except ValidationError:
            pass

    def test_regex(self):
        import re

        good_data = [
            {'path': ','},
            {'path': ',12345678-1234-1234-1234-123456789012,'},
            {'path': ',12345678-1234-1234-1234-123456789012,87654321-4321-4321-210987654321,'}
        ]
        bad_data = [
            {'path': ''},
            {'path': '12345678-1234-1234-1234-123456789012'},
            {'path': ',1234567-1234-1234-1234-123456789012,'}
        ]
        regex = re.compile(r',((urn:uuid:)?\w{8}-\w{4}-\w{4}-\w{4}-\w{12})*')
        Regex = class_generator(
            path=fields.Str(validate=validate.Regexp(regex))
        )
        good = Regex.load(good_data)
        assert set([x['path'] for x in good_data]) == set([x.path for x in good])
        try:
            bad = Regex.load(bad_data)
        except ValidationError:
            pass

    def test_uuid(self):
        pass

    def test_url(self):
        pass

    def test_nested(self):
        data = {
            'name': "Charles Dickens",
            'publications': [
                {
                    'title': "A Tale of Two Cities",
                    'year': 1859
                },
                {
                    'title': "A Christmas Carol",
                    'year': 1843
                }
            ]
        }
        Book = class_generator(
            title=fields.Str(),
            year=fields.Int()
        )
        Author = class_generator(
            name=fields.Str(),
            publications=fields.List(fields.Nested(Book.schema))
        )
        good = Author.load(data)
        assert good.name == data['name']
        assert [p.dump() for p in good.publications] == data['publications']
