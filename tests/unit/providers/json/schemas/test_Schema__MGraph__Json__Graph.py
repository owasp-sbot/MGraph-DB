from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge    import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node    import Schema__MGraph__Json__Node
from osbot_utils.utils.Objects                                      import type_full_name
from osbot_utils.testing.__                                         import __

from osbot_utils.utils.Dev import pprint

from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph


class test_Schema__MGraph__Json__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema_graph = Schema__MGraph__Json__Graph()

    def test__init__(self):
        with self.schema_graph as _:
            assert _.obj() == __(graph_data   = __(root_id=None),
                                 graph_id     = _.graph_id  ,
                                 graph_type   = type_full_name(Schema__MGraph__Json__Graph),
                                 schema_types = __(edge_type        = type_full_name(Schema__MGraph__Json__Edge   ),
                                                   graph_data_type  = type_full_name(Schema__MGraph__Graph__Data  ),
                                                   node_type        = type_full_name(Schema__MGraph__Json__Node   ),
                                                   node_data_type   = type_full_name(Schema__MGraph__Node__Data   )),
                                 edges        = __() ,
                                 nodes        = __() )


    def test__regression__from_json(self):
        with self.schema_graph as _:
            #error_message = "Invalid type for attribute 'graph_type'. Expected 'typing.Type[ForwardRef('Schema__MGraph__Graph')]' but got '<class 'str'>'"
            # with pytest.raises(ValueError, match=re.escape(error_message)):
            #     Schema__MGraph__Json__Graph.from_json(_.json())           # Fixed: BUG should had worked
            original_json = _.json()
            round_trip    = Schema__MGraph__Json__Graph.from_json(original_json)
            assert type(round_trip)      == Schema__MGraph__Json__Graph
            assert round_trip.graph_type == Schema__MGraph__Json__Graph
            assert round_trip.json()     == original_json
