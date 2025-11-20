import unittest

from osbot_utils.utils.Objects import full_type_name

from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data    import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.testing.__                                                      import __


class test_Schema__MGraph__Json__Node__Value(unittest.TestCase):
    def test__init__(self):                                                                         # Test Value node initialization
        with Schema__MGraph__Json__Node__Value() as _:
            assert _.obj() == __(node_data  =__(value      = None   ,
                                                value_type = None   ),
                                 node_type  = full_type_name(Schema__MGraph__Json__Node__Value),
                                 node_id    = _.node_id)

    def test_value_node_creation(self):                                                             # Test creating a value node with different types of values
        test_cases = [ ("hello"   , str       ),
                       (42        , int       ),
                       (3.14      , float     ),
                       (True      , bool      ),
                       (None      , type(None))]

        for value, expected_type in test_cases:
            node_data = Schema__MGraph__Json__Node__Value__Data(value=value,
                                                                value_type=expected_type)
            node = Schema__MGraph__Json__Node__Value(node_data=node_data)

            assert node.node_data.value      == value
            assert node.node_data.value_type == expected_type
            assert node.node_type            == Schema__MGraph__Json__Node__Value
