from unittest                                                           import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value import Schema__MGraph__Json__Node__Value
from osbot_utils.utils.Objects                                          import type_full_name
from osbot_utils.testing.__                                             import __
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value


class test_Domain__MGraph__Json__Node__Value(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Initialize test data
        cls.domain_node_value = Domain__MGraph__Json__Node__Value()

    def test__init__(self):                                                                 # Test basic initialization
        with self.domain_node_value as _:
            assert type(_)                                   is Domain__MGraph__Json__Node__Value
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node  = __(data=__(node_data  = __(value=None, value_type=None)                 ,
                                                    node_id    = _.node_id                                       ,
                                                    node_type  = type_full_name(Schema__MGraph__Json__Node__Value))),
                                 graph = _.graph.obj())

    def test_value_handling(self):                                                          # Test value node properties

        with self.domain_node_value as _:
            assert _.value      is None
            assert _.value_type is None
            _.value = "test_string"
            assert _.value          == "test_string"
            assert _.value_type     == str
            assert _.is_primitive() is True
            _.value = 123
            assert _.value          == 123
            assert _.value_type     == int
            assert _.is_primitive() is True

        # todo: BUG: capture case that with shallow ctor , (value=test_value, value_type=str) is not supported
        # test_value = "test_string"
        # node       = Domain__MGraph__Json__Node__Value(value=test_value, value_type=str)
        #
        # assert isinstance(node, Domain__MGraph__Json__Node__Value)
        # assert node.value          == test_value
        # assert node.value_type     == str
        # assert node.is_primitive() is True