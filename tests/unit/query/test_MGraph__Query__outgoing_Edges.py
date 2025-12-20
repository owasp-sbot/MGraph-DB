from unittest                               import TestCase
from mgraph_db.query.MGraph__Query          import MGraph__Query
from mgraph_db.mgraph.actions.MGraph__Data  import MGraph__Data
from mgraph_db.mgraph.index.MGraph__Index   import MGraph__Index
from mgraph_db.mgraph.MGraph                import MGraph


class test_MGraph__Query__outgoing_Edges(TestCase):

    def setUp(self):
        self.mgraph = MGraph()

        with self.mgraph.edit() as edit:
            self.node_a = edit.new_node()
            self.node_b = edit.new_node()
            self.node_c = edit.new_node()
            self.node_d = edit.new_node()

            self.edge_ab = edit.connect_nodes(from_node=self.node_a, to_node=self.node_b)
            self.edge_bc = edit.connect_nodes(from_node=self.node_b, to_node=self.node_c)
            self.edge_cd = edit.connect_nodes(from_node=self.node_c, to_node=self.node_d)

        self.mgraph_index = MGraph__Index.from_graph(self.mgraph.graph)
        self.mgraph_data  = MGraph__Data(graph=self.mgraph.graph)
        self.query        = MGraph__Query(mgraph_index = self.mgraph_index ,
                                          mgraph_data  = self.mgraph_data  ).setup()

    def test_add_outgoing_edges__from_single_node(self):                         # Test adding outgoing edges
        with self.query as _:
            _.create_view(nodes_ids = {self.node_a.node_id} ,
                          edges_ids = set()                 ,
                          operation = 'start'               ,
                          params    = {}                    )

            _.add_outgoing_edges()

            current_nodes = _.nodes_ids()
            current_edges = _.edges_ids()

            assert self.node_a.node_id    in current_nodes
            assert self.node_b.node_id    in current_nodes                       # Added via edge
            assert self.edge_ab.edge_id   in current_edges

    def test_add_outgoing_edges__no_outgoing(self):                              # Test node with no outgoing
        with self.query as _:
            _.create_view(nodes_ids = {self.node_d.node_id} ,                    # Last node in chain
                          edges_ids = set()                 ,
                          operation = 'start'               ,
                          params    = {}                    )

            _.add_outgoing_edges()

            current_nodes = _.nodes_ids()

            assert len(current_nodes) == 1                                       # Only original node
            assert self.node_d.node_id in current_nodes

    def test_add_outgoing_edges__with_depth(self):                               # Test with depth parameter
        with self.query as _:
            _.create_view(nodes_ids = {self.node_a.node_id} ,
                          edges_ids = set()                 ,
                          operation = 'start'               ,
                          params    = {}                    )

            _.add_outgoing_edges__with_depth(depth=2)

            current_nodes = _.nodes_ids()

            assert self.node_a.node_id in current_nodes
            assert self.node_b.node_id in current_nodes                          # Depth 1
            assert self.node_c.node_id in current_nodes                          # Depth 2

    def test_add_outgoing_edges__with_depth_zero(self):                          # Test with depth=0
        with self.query as _:
            _.create_view(nodes_ids = {self.node_a.node_id} ,
                          edges_ids = set()                 ,
                          operation = 'start'               ,
                          params    = {}                    )

            _.add_outgoing_edges__with_depth(depth=0)

            current_nodes = _.nodes_ids()

            assert len(current_nodes) == 1