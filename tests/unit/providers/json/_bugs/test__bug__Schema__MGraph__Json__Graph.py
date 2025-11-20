from unittest                                                                   import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data   import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.utils.Objects                                                  import full_type_name
from osbot_utils.testing.__                                                     import __
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                        import Schema__MGraph__Node__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph               import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value         import Schema__MGraph__Json__Node__Value

class test_Schema__MGraph__Json__Graph__Bug(TestCase):

    def test___bug__from_json__node_data__not_preserved(self):
        value_node      = Schema__MGraph__Json__Node__Value(node_data=dict(value="test_value", value_type=str))
        value_node_json = value_node.json()
        node_id         = value_node.node_id

        graph                           = Schema__MGraph__Json__Graph()
        graph.nodes[value_node.node_id] = value_node
        graph_json                      = graph.json()
        graph_round_trip                = Schema__MGraph__Json__Graph.from_json(graph_json)
        assert type(graph_round_trip.nodes[node_id].node_data)             is Schema__MGraph__Json__Node__Value__Data                           # Fixed: BUG node has the wront type
        assert type(graph_round_trip.nodes[node_id].node_data)             is not     Schema__MGraph__Node__Data                                # Fixed: BUG wrong type
        assert graph_round_trip.nodes[value_node.node_id].node_data.json() != {}                                                                # Fixed: BUG should not be {}
        assert graph_round_trip.nodes[value_node.node_id].node_data.json() == {'value': 'test_value', 'value_type': 'builtins.str'}             # Fixed
        assert Schema__MGraph__Json__Graph.from_json(graph_json).json()    == graph_json                                                        # Fixed: BUG should be equal
        assert graph_round_trip.nodes[value_node.node_id].obj()            == __(node_data=__(value='test_value', value_type='builtins.str'),   # BUG should not be empty
                                                                                 node_id=node_id,
                                                                                 node_type=full_type_name(Schema__MGraph__Json__Node__Value)) # node_type is correct Schema__MGraph__Json__Node__Value

