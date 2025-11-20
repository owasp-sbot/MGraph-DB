import unittest

from osbot_utils.utils.Objects                                                   import full_type_name
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data import Schema__MGraph__Json__Node__Property__Data
from osbot_utils.testing.__                                                      import __


class test_Schema__MGraph__Json__Node__Property(unittest.TestCase):
    def test__init__(self):                                                                         # Test Property node initialization
        with Schema__MGraph__Json__Node__Property() as _:
            assert _.obj() == __(node_data  =__(name=''),
                                 node_type  = full_type_name(Schema__MGraph__Json__Node__Property),
                                 node_id    = _.node_id)

    def test_property_node_creation(self):                                                          # Test creating a property node
        node_data = Schema__MGraph__Json__Node__Property__Data(name='test_property')
        node = Schema__MGraph__Json__Node__Property(node_data=node_data)

        assert node.node_data.name  == "test_property"
        assert node.node_type       == Schema__MGraph__Json__Node__Property

    def test_property_node_name_change(self):                                                       # Test changing a property node's name
        node_data = Schema__MGraph__Json__Node__Property__Data(name='original_name')
        node = Schema__MGraph__Json__Node__Property(node_data=node_data)

        node.node_data.name = "new_name"
        assert node.node_data.name == "new_name"