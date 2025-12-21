from unittest                                                       import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Edges                    import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                   import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Edit                     import MGraph__Index__Edit
from mgraph_db.mgraph.index.MGraph__Index__Paths                    import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Types                    import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                   import MGraph__Index__Values
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data     import Schema__MGraph__Index__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class test_MGraph__Index__Edit(TestCase):

    def setUp(self):
        self.index_data      = Schema__MGraph__Index__Data()
        self.edges_index     = MGraph__Index__Edges (index_data=self.index_data)
        self.labels_index    = MGraph__Index__Labels(index_data=self.index_data)
        self.paths_index     = MGraph__Index__Paths (index_data=self.index_data)
        self.types_index     = MGraph__Index__Types (index_data=self.index_data)
        self.values_index    = MGraph__Index__Values()
        self.resolver        = MGraph__Type__Resolver()
        self.edit_index = MGraph__Index__Edit(
            index_data   = self.index_data   ,
            edges_index  = self.edges_index  ,
            labels_index = self.labels_index ,
            paths_index  = self.paths_index  ,
            types_index  = self.types_index  ,
            values_index = self.values_index ,
            resolver     = self.resolver     )

    def test__init__(self):
        with self.edit_index as _:
            assert type(_)              is MGraph__Index__Edit
            assert type(_.index_data)   is Schema__MGraph__Index__Data
            assert type(_.edges_index)  is MGraph__Index__Edges
            assert type(_.labels_index) is MGraph__Index__Labels
            assert type(_.paths_index)  is MGraph__Index__Paths
            assert type(_.types_index)  is MGraph__Index__Types
            assert type(_.values_index) is MGraph__Index__Values
            assert type(_.resolver)     is MGraph__Type__Resolver

    # =========================================================================
    # Add Node Tests
    # =========================================================================

    def test_add_node(self):
        node = Schema__MGraph__Node().set_node_type()

        with self.edit_index as _:
            _.add_node(node)

            # Verify node was indexed
            assert node.node_id in self.edges_index.nodes_to_outgoing_edges()
            assert node.node_id in self.edges_index.nodes_to_incoming_edges()
            assert 'Schema__MGraph__Node' in self.types_index.nodes_by_type()
            assert node.node_id in self.types_index.nodes_by_type()['Schema__MGraph__Node']

    def test_add_node__multiple(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)

            assert len(self.types_index.nodes_by_type()['Schema__MGraph__Node']) == 2

    # =========================================================================
    # Remove Node Tests
    # =========================================================================

    def test_remove_node(self):
        node = Schema__MGraph__Node().set_node_type()

        with self.edit_index as _:
            _.add_node(node)
            _.remove_node(node)

            # Verify node was removed
            assert node.node_id not in self.edges_index.nodes_to_outgoing_edges()
            assert node.node_id not in self.edges_index.nodes_to_incoming_edges()
            assert 'Schema__MGraph__Node' not in self.types_index.nodes_by_type()

    def test_remove_node__with_edges(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            # Verify edge exists
            assert edge.edge_id in self.edges_index.edges_to_nodes()

            _.remove_node(node_1)

            # Verify edge was also removed
            assert edge.edge_id not in self.edges_index.edges_to_nodes()
            assert node_1.node_id not in self.edges_index.nodes_to_outgoing_edges()

    # =========================================================================
    # Add Edge Tests
    # =========================================================================

    def test_add_edge(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            # Verify edge was indexed
            assert edge.edge_id in self.edges_index.edges_to_nodes()
            assert self.edges_index.edges_to_nodes()[edge.edge_id] == (node_1.node_id, node_2.node_id)
            assert edge.edge_id in self.edges_index.nodes_to_outgoing_edges()[node_1.node_id]
            assert edge.edge_id in self.edges_index.nodes_to_incoming_edges()[node_2.node_id]
            assert 'Schema__MGraph__Edge' in self.types_index.edges_by_type()

    def test_add_edge__multiple(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()
        edge_2 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            assert len(self.edges_index.edges_to_nodes()) == 2
            assert len(self.edges_index.nodes_to_outgoing_edges()[node_1.node_id]) == 2

    # =========================================================================
    # Remove Edge Tests
    # =========================================================================

    def test_remove_edge(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)
            _.remove_edge(edge)

            # Verify edge was removed
            assert edge.edge_id not in self.edges_index.edges_to_nodes()
            assert edge.edge_id not in self.edges_index.nodes_to_outgoing_edges().get(node_1.node_id, set())
            assert edge.edge_id not in self.edges_index.nodes_to_incoming_edges().get(node_2.node_id, set())

    def test_remove_edge_by_id(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)
            _.remove_edge_by_id(edge.edge_id)

            assert edge.edge_id not in self.edges_index.edges_to_nodes()

    def test_remove_edge_by_id__nonexistent(self):
        with self.edit_index as _:
            _.remove_edge_by_id(Edge_Id(Obj_Id()))                              # Should not crash

            assert True

    def test_remove_edge__keeps_nodes(self):
        node_1 = Schema__MGraph__Node().set_node_type()
        node_2 = Schema__MGraph__Node().set_node_type()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)
            _.remove_edge(edge)

            # Nodes should still exist
            assert node_1.node_id in self.types_index.nodes_by_type()['Schema__MGraph__Node']
            assert node_2.node_id in self.types_index.nodes_by_type()['Schema__MGraph__Node']

    # =========================================================================
    # Edge Case Tests
    # =========================================================================

    def test_add_remove_add_same_node(self):
        node = Schema__MGraph__Node().set_node_type()

        with self.edit_index as _:
            _.add_node(node)
            _.remove_node(node)
            _.add_node(node)                                                    # Re-add same node

            assert node.node_id in self.types_index.nodes_by_type()['Schema__MGraph__Node']

    def test_chain_of_edges(self):
        node_a = Schema__MGraph__Node().set_node_type()
        node_b = Schema__MGraph__Node().set_node_type()
        node_c = Schema__MGraph__Node().set_node_type()
        edge_1 = Schema__MGraph__Edge(from_node_id=node_a.node_id, to_node_id=node_b.node_id).set_edge_type()
        edge_2 = Schema__MGraph__Edge(from_node_id=node_b.node_id, to_node_id=node_c.node_id).set_edge_type()

        with self.edit_index as _:
            _.add_node(node_a)
            _.add_node(node_b)
            _.add_node(node_c)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            # Node B should have both incoming and outgoing
            assert edge_1.edge_id in self.edges_index.nodes_to_incoming_edges()[node_b.node_id]
            assert edge_2.edge_id in self.edges_index.nodes_to_outgoing_edges()[node_b.node_id]

            # Remove middle node
            _.remove_node(node_b)

            # Both edges should be removed
            assert edge_1.edge_id not in self.edges_index.edges_to_nodes()
            assert edge_2.edge_id not in self.edges_index.edges_to_nodes()