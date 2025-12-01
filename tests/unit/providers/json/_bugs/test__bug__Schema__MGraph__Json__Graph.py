from unittest                                                                   import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                              import Schema__MGraph__Node

from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data   import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
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
        node_id_str     = str(node_id)                                                                                                          # Convert to primitive string for comparison

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
                                                                                 node_id=node_id_str,
                                                                                 node_type=full_type_name(Schema__MGraph__Json__Node__Value))   # node_type is correct Schema__MGraph__Json__Node__Value


    def test___regression__from_json__round_trip__with_predefined_ids(self):  # Pre-defined IDs for deterministic testing
        node_id  = 'a1234567'
        graph_id = 'b2345678'

        # Create value node with pre-defined node_id
        value_node           = Schema__MGraph__Json__Node__Value(node_id=node_id)
        value_node.node_data = Schema__MGraph__Json__Node__Value__Data(value="test_value", value_type=str)

        # Create graph with pre-defined graph_id
        graph                    = Schema__MGraph__Json__Graph(graph_id=graph_id)
        graph.nodes[node_id]     = value_node

        # Get JSON representation
        graph_json = graph.json()

        assert graph.json() == {'edges': {},
                             'graph_data': {'root_id': None},
                             'graph_id': 'b2345678',
                             'graph_type': 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph.Schema__MGraph__Json__Graph',
                             'nodes': {'a1234567': {'node_data': {'value': 'test_value',
                                                                  'value_type': 'builtins.str'},
                                                    'node_id': 'a1234567',
                                                    'node_type': 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value.Schema__MGraph__Json__Node__Value'}},
                             'schema_types': {'edge_type': 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge.Schema__MGraph__Json__Edge',
                                              'graph_data_type': 'mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                              'node_data_type': 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data',
                                              'node_type': 'mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node'}}
        assert graph.obj() == __(graph_data=__(root_id=None),
                                graph_id='b2345678',
                                graph_type='mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph.Schema__MGraph__Json__Graph',
                                schema_types=__(edge_type='mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge.Schema__MGraph__Json__Edge',
                                                graph_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                node_type='mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node',
                                                node_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'),
                                edges=__(),
                                nodes=__(a1234567=__(node_data=__(value='test_value',
                                                                  value_type='builtins.str'),
                                                     node_id='a1234567',
                                                     node_type='mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value.Schema__MGraph__Json__Node__Value')))

        graph_round_trip = Schema__MGraph__Json__Graph.from_json(graph_json)
        assert graph_round_trip.json() == graph_json
        assert graph_round_trip.json() == graph.json()
        assert graph_round_trip.obj () == graph.obj()

    def test___regression__from_json__round_trip__with_node_id_instance_as_key(self):
        # Pre-defined IDs for deterministic testing
        node_id  = Node_Id('a1234567')  # Use Node_Id instance, not str
        graph_id = 'b2345678'

        # Create value node with pre-defined node_id
        value_node           = Schema__MGraph__Json__Node__Value(node_id=node_id)
        value_node.node_data = Schema__MGraph__Json__Node__Value__Data(value="test_value", value_type=str)

        # Create graph with pre-defined graph_id
        graph                = Schema__MGraph__Json__Graph(graph_id=graph_id)
        graph.nodes[node_id] = value_node  # Using Node_Id instance as key

        # Get JSON representation
        graph_json = graph.json()

        # Round-trip
        graph_round_trip      = Schema__MGraph__Json__Graph.from_json(graph_json)
        graph_round_trip_json = graph_round_trip.json()

        # This assertion should fail - showing the bug
        assert graph_round_trip_json == graph_json  # FIXED: BUG Fails here

    def test___regression__roundtrip__from_json__node(self):
        node_id = Node_Id('a1234567')
        node    = Schema__MGraph__Node(node_id=node_id)

        assert node.node_id == 'a1234567'
        assert node.node_id == node_id
        assert node.json()  == { 'node_data': {},
                                 'node_id': 'a1234567',
                                 'node_type': 'mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node'}
        assert node.obj()   == __( node_data=__(),
                                   node_id='a1234567',
                                   node_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node') != __()

        roundtrip = Schema__MGraph__Node.from_json(node.json())
        assert roundtrip.json() == node.json()
        assert roundtrip.obj () == node.obj()

        def test_node_class(node_class):
            assert node_class.from_json(node_class(node_id=node_id).json()).json() == node_class(node_id=node_id).json()

        test_node_class(Schema__MGraph__Node)
        test_node_class(Schema__MGraph__Json__Node__Value)


    def test__regression__roundtrip__on_graph__using__nodes_assignment(self):
        node_id_value = 'a1234567'
        node_id       = Node_Id(node_id_value)  # Use Node_Id instance, not str
        graph_id      = 'b2345678'
        node    = Schema__MGraph__Node(node_id=node_id)
        graph_1                = Schema__MGraph__Json__Graph(graph_id=graph_id)
        graph_1.nodes[node_id] = node
        graph_1_json             = graph_1.json()
        #assert type(graph_1_json['nodes'][node_id]) == dict                 # BUG: node_id is of type Node_Id
        error_message = "'a1234567'"
        #with pytest.raises(KeyError, match=re.escape(error_message)):
        #    graph_1_json['nodes'][node_id_value]                            # BUG: this should work since
        assert type(graph_1_json['nodes'][node_id_value]) == dict            # FIXED

        # assert graph_1_json['nodes'] == {node_id       : node.json()}         # BUG: node_id should not work as a key
        # assert graph_1_json['nodes'] != {node_id_value : node.json()}       # BUG: node_id_value should work as a key
        assert graph_1_json['nodes'] != {node_id       : node.json()}       # FIXED
        assert graph_1_json['nodes'] == {node_id_value : node.json()}       # FIXED
        #assert Schema__MGraph__Json__Graph.from_json(graph_1_json).json() != graph_1_json # BUG: should be the same
        assert Schema__MGraph__Json__Graph.from_json(graph_1_json).json() == graph_1_json