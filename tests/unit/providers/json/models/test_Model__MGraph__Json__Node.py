import unittest
from mgraph_db.providers.json.models.Model__MGraph__Json__Node   import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from osbot_utils.utils.Objects                                   import type_full_name
from osbot_utils.testing.__                                      import __


class test_Model__MGraph__Json__Node(unittest.TestCase):
    def test_init(self):                                                                                # Test base JSON node model initialization
        with Model__MGraph__Json__Node(data=Schema__MGraph__Json__Node()) as _:                         # Create base JSON node model
            assert _.obj()                == __(data=__(node_data  = __()     ,
                                                        node_id    = _.node_id,
                                                        node_type  = type_full_name(Schema__MGraph__Json__Node)))
            assert _.data.node_type       == Schema__MGraph__Json__Node
            assert _.obj().data.node_type == type_full_name(Schema__MGraph__Json__Node)
            assert _.obj().data.node_type == 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node'

