from unittest                                                 import TestCase
from mgraph_db.providers.json.MGraph__Json                    import MGraph__Json
from osbot_utils.helpers.duration.decorators.capture_duration import capture_duration


class test__regression__Domain__MGraph__Json__Node__Dict(TestCase):                     # Test that captures the property visibility bug

    def test__regression__performance__mgraph_json__load__from_json(self):

        mgraph_json = MGraph__Json()

        json_data = { "string" : "value"         ,
                      "number" : 42              ,
                      "boolean": True            ,
                      "null"   : None            ,
                      "array"  : [1, 2, 3]       ,
                      "object" : {"key": "value"}}

        source_json = {'a': json_data, 'b': json_data,
                       'c': json_data, 'd': json_data,
                       'e': json_data, 'f': json_data,
                       'g': json_data, 'h': json_data}

        with capture_duration() as duration:
            mgraph_json.load().from_data(source_json)
        #assert 0.5 < duration.seconds < 1                      # BUG
        assert 0    <= duration.seconds < 0.2                    # Fixed

