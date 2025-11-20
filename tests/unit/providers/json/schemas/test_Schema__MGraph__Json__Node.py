import unittest
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node                 import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict           import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List           import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from osbot_utils.testing.__                                                      import __

class test_Schema__MGraph__Json__Node(unittest.TestCase):
    def test__init__(self):                                                                         # Test base JSON node initialization
        with Schema__MGraph__Json__Node() as _:
            assert _.obj() == __(node_data  =__(),
                                 node_type  = 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node',
                                 node_id    = _.node_id)

    def test_base_node_inheritance(self):                                                           # Verify that all specific node types inherit from base JSON node
        node_classes = [Schema__MGraph__Json__Node__Value   ,
                        Schema__MGraph__Json__Node__Dict    ,
                        Schema__MGraph__Json__Node__List    ,
                        Schema__MGraph__Json__Node__Property]

        for node_class in node_classes:
            assert issubclass(node_class, Schema__MGraph__Json__Node), \
                f"{node_class.__name__} should inherit from Schema__MGraph__Json__Node"



