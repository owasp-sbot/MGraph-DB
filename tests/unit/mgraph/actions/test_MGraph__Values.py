from unittest                                                import TestCase
from mgraph_db.mgraph.MGraph                                 import MGraph
from mgraph_db.mgraph.actions.MGraph__Values                 import MGraph__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge
from osbot_utils.utils.Env                                   import load_dotenv


class test_MGraph__Values(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = False                                                                      # set to true to create a screenshot per test
        cls.screenshot_file = './mgraph-values.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.mgraph = MGraph()                                                                           # Create fresh graph for each test
        self.values = MGraph__Values(mgraph_edit=self.mgraph.edit())

    def tearDown(self):
        if self.screenshot_create:
            with self.mgraph.screenshot(target_file=self.screenshot_file) as screenshot:
                with screenshot.export().export_dot() as _:
                    #_.show_node__value()
                    #_.show_edge__id()
                    pass
                with screenshot as _:
                    _.save_to(self.screenshot_file)
                    _.dot()

    def test_get_or_create(self):                                                                       # Test direct node creation
        value_node_1 = self.values.get_or_create(42)                                                    # Create int node
        value_node_2 = self.values.get_or_create(42)                                                    # Get same node
        node_id      = value_node_1.node_id
        node_id_str  = str(node_id)                                                                     # Convert to primitive string for JSON comparison

        assert self.mgraph.index().values_index.index_data.json() == { 'hash_to_node'  : {'f8bb59eae6'  : node_id_str}  ,
                                                                       'node_to_hash'  : {node_id_str   : 'f8bb59eae6'} ,
                                                                       'type_by_value' : {'f8bb59eae6'  : 'builtins.int'},
                                                                       'values_by_type': {'builtins.int': ['f8bb59eae6']}}
        assert self.mgraph.index().index_data.json()              == { 'edges_by_incoming_label'        : {}                                              ,
                                                                       'edges_by_outgoing_label'        : {}                                              ,
                                                                       'edges_by_path'                  : {}                                              ,   # NEW: path index
                                                                       'edges_by_predicate'             : {}                                              ,
                                                                       'edges_by_type'                  : {}                                              ,
                                                                       'edges_incoming_labels'          : {}                                              ,
                                                                       'edges_outgoing_labels'          : {}                                              ,
                                                                       'edges_predicates'               : {}                                              ,
                                                                       'edges_to_nodes'                 : {}                                              ,
                                                                       'edges_types'                    : {}                                              ,
                                                                       'nodes_by_path'                  : {}                                              ,   # NEW: path index
                                                                       'nodes_by_type'                  : {'Schema__MGraph__Node__Value': [node_id_str]}  ,
                                                                       'nodes_to_incoming_edges'        : {node_id_str: []}                            ,
                                                                       'nodes_to_incoming_edges_by_type': {}                                              ,
                                                                       'nodes_to_outgoing_edges'        : {node_id_str: []}                            ,
                                                                       'nodes_to_outgoing_edges_by_type': {}                                              ,
                                                                       'nodes_types'                    : {node_id_str: 'Schema__MGraph__Node__Value'}}

        assert value_node_1.node_id         == value_node_2.node_id                                     # Verify node reuse and correct value
        assert value_node_1.node_data.value == "42"                                                     # Note: value stored as string
        assert value_node_1.node_data.value_type is int                                                 # But type maintained

        str_node_1 = self.values.get_or_create("test")                                                   # Test with string values
        str_node_2 = self.values.get_or_create("test")

        assert str_node_1.node_id           == str_node_2.node_id
        assert str_node_1.node_data.value   == "test"
        assert str_node_1.node_data.value_type is str

    def test_get_or_create_value(self):
        class Test_Edge(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_node = _.new_node()

            value_node_1, edge_1 = self.values.get_or_create_value(42, Test_Edge, root_node)
            value_node_2, edge_2 = self.values.get_or_create_value(42, Test_Edge, root_node)

            # Verify value node reuse
            assert value_node_1.node_id              == value_node_2.node_id
            assert edge_1.edge_id                    == edge_2.edge_id                       #confirm we get the same edge
            assert value_node_1.node_data.value      == "42"
            assert value_node_1.node_data.value_type is int

    def test_get_linked_value(self):
        class Test_Edge(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_node = _.new_node()
            value_node, _ = self.values.get_or_create_value("test", Test_Edge, root_node)

            linked_node = self.values.get_linked_value(root_node, Test_Edge)
            assert linked_node.node_id              == value_node.node_id
            assert linked_node.node_data.value      == "test"
            assert linked_node.node_data.value_type is str

    def test_multiple_edges_to_value(self):
        class Edge_1(Schema__MGraph__Edge): pass
        class Edge_2(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_1 = _.new_node()
            root_2 = _.new_node()

            value_1, edge_1 = self.values.get_or_create_value(42, Edge_1, root_1)
            value_2, edge_2 = self.values.get_or_create_value(42, Edge_2, root_2)

            assert value_1.node_id              == value_2.node_id                      # Verify value node reuse across different edges
            assert edge_1.edge_id               != edge_2.edge_id
            assert value_1.node_data.value      == "42"
            assert value_1.node_data.value_type is int


            value_1_linked = self.values.get_linked_value(root_1, Edge_1)               # Test retrieval
            value_2_linked = self.values.get_linked_value(root_2, Edge_2)
            assert value_1_linked.node_id         == value_2_linked.node_id
            assert value_1_linked.node_data.value == "42"

    def test_get_by_hash(self):
        value_node = self.values.get_or_create(42)
        value_hash = self.mgraph.index().values_index.calculate_hash(int, "42", node_type=type(value_node.node.data))

        retrieved_node = self.values.get_by_hash(value_hash)
        assert retrieved_node.node_id              == value_node.node_id
        assert retrieved_node.node_data.value      == "42"
        assert retrieved_node.node_data.value_type is int

    def test_get_by_value(self):
        value_node     = self.values.get_or_create(42)
        retrieved_node = self.values.get_by_value(int, "42")
        assert retrieved_node.node_id              == value_node.node_id
        assert retrieved_node.node_data.value      == "42"
        assert retrieved_node.node_data.value_type is int