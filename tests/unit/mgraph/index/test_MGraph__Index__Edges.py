from unittest                                                       import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Edges                    import MGraph__Index__Edges
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data     import Schema__MGraph__Index__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class test_MGraph__Index__Edges(TestCase):

    def setUp(self):
        self.index_data  = Schema__MGraph__Index__Data()
        self.edges_index = MGraph__Index__Edges(index_data=self.index_data)

    def test__init__(self):                                                     # Test initialization
        with self.edges_index as _:
            assert type(_)            is MGraph__Index__Edges
            assert type(_.index_data) is Schema__MGraph__Index__Data
            assert _.edges_to_nodes()          == {}
            assert _.nodes_to_outgoing_edges() == {}
            assert _.nodes_to_incoming_edges() == {}

    # =========================================================================
    # Node Edge Sets - Initialize Tests
    # =========================================================================

    def test_init_node_edge_sets(self):                                         # Test initializing node edge sets
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.init_node_edge_sets(node_id)

            assert node_id in _.nodes_to_outgoing_edges()
            assert node_id in _.nodes_to_incoming_edges()
            assert _.nodes_to_outgoing_edges()[node_id] == set()
            assert _.nodes_to_incoming_edges()[node_id] == set()

    def test_init_node_edge_sets__idempotent(self):                             # Test that init is idempotent
        node_id = Node_Id(Obj_Id())
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.init_node_edge_sets(node_id)
            _.nodes_to_outgoing_edges()[node_id].add(edge_id)                   # Add an edge
            _.init_node_edge_sets(node_id)                                      # Init again

            assert edge_id in _.nodes_to_outgoing_edges()[node_id]              # Edge should still be there

    # =========================================================================
    # Edge-Node Mapping - Add Tests
    # =========================================================================

    def test_index_edge(self):                                                  # Test indexing an edge
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, from_node_id, to_node_id)

            assert edge_id in _.edges_to_nodes()
            assert _.edges_to_nodes()[edge_id] == (from_node_id, to_node_id)
            assert edge_id in _.nodes_to_outgoing_edges()[from_node_id]
            assert edge_id in _.nodes_to_incoming_edges()[to_node_id]

    def test_index_edge__multiple_edges_same_nodes(self):                       # Test multiple edges between same nodes
        edge_id_1    = Edge_Id(Obj_Id())
        edge_id_2    = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id_1, from_node_id, to_node_id)
            _.index_edge(edge_id_2, from_node_id, to_node_id)

            assert len(_.nodes_to_outgoing_edges()[from_node_id]) == 2
            assert len(_.nodes_to_incoming_edges()[to_node_id])   == 2
            assert edge_id_1 in _.nodes_to_outgoing_edges()[from_node_id]
            assert edge_id_2 in _.nodes_to_outgoing_edges()[from_node_id]

    def test_index_edge__chain(self):                                           # Test chain of edges A -> B -> C
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        node_c    = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id_1, node_a, node_b)
            _.index_edge(edge_id_2, node_b, node_c)

            # Node B should have both incoming and outgoing
            assert edge_id_1 in _.nodes_to_incoming_edges()[node_b]
            assert edge_id_2 in _.nodes_to_outgoing_edges()[node_b]

    # =========================================================================
    # Edge-Node Mapping - Remove Tests
    # =========================================================================

    def test_remove_node_edge_sets(self):                                       # Test removing node edge sets
        node_id      = Node_Id(Obj_Id())
        edge_id_out  = Edge_Id(Obj_Id())
        edge_id_in   = Edge_Id(Obj_Id())
        other_node_1 = Node_Id(Obj_Id())
        other_node_2 = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id_out, node_id, other_node_1)
            _.index_edge(edge_id_in, other_node_2, node_id)

            outgoing, incoming = _.remove_node_edge_sets(node_id)

            assert edge_id_out in outgoing
            assert edge_id_in  in incoming
            assert node_id not in _.nodes_to_outgoing_edges()
            assert node_id not in _.nodes_to_incoming_edges()

    def test_remove_node_edge_sets__empty(self):                                # Test removing nonexistent node
        with self.edges_index as _:
            outgoing, incoming = _.remove_node_edge_sets(Node_Id(Obj_Id()))

            assert outgoing == set()
            assert incoming == set()

    def test_remove_edge(self):                                                 # Test removing an edge
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, from_node_id, to_node_id)
            result = _.remove_edge(edge_id)

            assert result == (from_node_id, to_node_id)
            assert edge_id not in _.edges_to_nodes()
            assert edge_id not in _.nodes_to_outgoing_edges().get(from_node_id, set())
            assert edge_id not in _.nodes_to_incoming_edges().get(to_node_id, set())

    def test_remove_edge__not_found(self):                                      # Test removing nonexistent edge
        with self.edges_index as _:
            result = _.remove_edge(Edge_Id(Obj_Id()))

            assert result is None

    def test_remove_edge__keeps_other_edges(self):                              # Test keeps other edges
        edge_id_1    = Edge_Id(Obj_Id())
        edge_id_2    = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id_1, from_node_id, to_node_id)
            _.index_edge(edge_id_2, from_node_id, to_node_id)
            _.remove_edge(edge_id_1)

            assert edge_id_1 not in _.edges_to_nodes()
            assert edge_id_2     in _.edges_to_nodes()
            assert edge_id_1 not in _.nodes_to_outgoing_edges()[from_node_id]
            assert edge_id_2     in _.nodes_to_outgoing_edges()[from_node_id]

    # =========================================================================
    # Edge Query Tests
    # =========================================================================

    def test_get_edge_nodes(self):                                              # Test get_edge_nodes
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, from_node_id, to_node_id)

            result = _.get_edge_nodes(edge_id)

            assert result == (from_node_id, to_node_id)

    def test_get_edge_nodes__not_found(self):                                   # Test get_edge_nodes with nonexistent edge
        with self.edges_index as _:
            result = _.get_edge_nodes(Edge_Id(Obj_Id()))

            assert result is None

    def test_get_edge_from_node(self):                                          # Test get_edge_from_node
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, from_node_id, to_node_id)

            result = _.get_edge_from_node(edge_id)

            assert result == from_node_id

    def test_get_edge_from_node__not_found(self):                               # Test with nonexistent edge
        with self.edges_index as _:
            result = _.get_edge_from_node(Edge_Id(Obj_Id()))

            assert result is None

    def test_get_edge_to_node(self):                                            # Test get_edge_to_node
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, from_node_id, to_node_id)

            result = _.get_edge_to_node(edge_id)

            assert result == to_node_id

    def test_has_edge(self):                                                    # Test has_edge
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, Node_Id(Obj_Id()), Node_Id(Obj_Id()))

            assert _.has_edge(edge_id)          is True
            assert _.has_edge(Edge_Id(Obj_Id())) is False

    def test_edge_count(self):                                                  # Test edge_count
        with self.edges_index as _:
            assert _.edge_count() == 0

            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()))
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()))
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()))

            assert _.edge_count() == 3

    # =========================================================================
    # Node Edge Query Tests
    # =========================================================================

    def test_get_node_outgoing_edges(self):                                     # Test get_node_outgoing_edges with node object
        node = Schema__MGraph__Node()
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, node.node_id, Node_Id(Obj_Id()))

            result = _.get_node_outgoing_edges(node)

            assert edge_id in result

    def test_get_node_id_outgoing_edges(self):                                  # Test get_node_id_outgoing_edges
        node_id = Node_Id(Obj_Id())
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, node_id, Node_Id(Obj_Id()))

            result = _.get_node_id_outgoing_edges(node_id)

            assert edge_id in result

    def test_get_node_id_outgoing_edges__not_found(self):                       # Test with nonexistent node
        with self.edges_index as _:
            result = _.get_node_id_outgoing_edges(Node_Id(Obj_Id()))

            assert result == set()

    def test_get_node_incoming_edges(self):                                     # Test get_node_incoming_edges with node object
        node = Schema__MGraph__Node()
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, Node_Id(Obj_Id()), node.node_id)

            result = _.get_node_incoming_edges(node)

            assert edge_id in result

    def test_get_node_id_incoming_edges(self):                                  # Test get_node_id_incoming_edges
        node_id = Node_Id(Obj_Id())
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, Node_Id(Obj_Id()), node_id)

            result = _.get_node_id_incoming_edges(node_id)

            assert edge_id in result

    def test_get_node_all_edges(self):                                          # Test get_node_all_edges
        node_id     = Node_Id(Obj_Id())
        edge_id_out = Edge_Id(Obj_Id())
        edge_id_in  = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id_out, node_id, Node_Id(Obj_Id()))
            _.index_edge(edge_id_in, Node_Id(Obj_Id()), node_id)

            result = _.get_node_all_edges(node_id)

            assert edge_id_out in result
            assert edge_id_in  in result
            assert len(result) == 2

    def test_count_node_outgoing_edges(self):                                   # Test count_node_outgoing_edges
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_id, Node_Id(Obj_Id()))
            _.index_edge(Edge_Id(Obj_Id()), node_id, Node_Id(Obj_Id()))

            assert _.count_node_outgoing_edges(node_id)          == 2
            assert _.count_node_outgoing_edges(Node_Id(Obj_Id())) == 0

    def test_count_node_incoming_edges(self):                                   # Test count_node_incoming_edges
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), node_id)
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), node_id)
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), node_id)

            assert _.count_node_incoming_edges(node_id) == 3

    def test_has_node_outgoing_edges(self):                                     # Test has_node_outgoing_edges
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            assert _.has_node_outgoing_edges(node_id) is False

            _.index_edge(Edge_Id(Obj_Id()), node_id, Node_Id(Obj_Id()))

            assert _.has_node_outgoing_edges(node_id) is True

    def test_has_node_incoming_edges(self):                                     # Test has_node_incoming_edges
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            assert _.has_node_incoming_edges(node_id) is False

            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), node_id)

            assert _.has_node_incoming_edges(node_id) is True

    # =========================================================================
    # Node Traversal Tests
    # =========================================================================

    def test_get_connected_nodes_outgoing(self):                                # Test get_connected_nodes_outgoing
        node_a  = Node_Id(Obj_Id())
        node_b  = Node_Id(Obj_Id())
        node_c  = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_b)
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_c)

            result = _.get_connected_nodes_outgoing(node_a)

            assert node_b in result
            assert node_c in result
            assert len(result) == 2

    def test_get_connected_nodes_outgoing__empty(self):                         # Test with no outgoing edges
        with self.edges_index as _:
            result = _.get_connected_nodes_outgoing(Node_Id(Obj_Id()))

            assert result == set()

    def test_get_connected_nodes_incoming(self):                                # Test get_connected_nodes_incoming
        node_a  = Node_Id(Obj_Id())
        node_b  = Node_Id(Obj_Id())
        node_c  = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_c)
            _.index_edge(Edge_Id(Obj_Id()), node_b, node_c)

            result = _.get_connected_nodes_incoming(node_c)

            assert node_a in result
            assert node_b in result
            assert len(result) == 2

    def test_get_all_connected_nodes(self):                                     # Test get_all_connected_nodes
        node_a  = Node_Id(Obj_Id())
        node_b  = Node_Id(Obj_Id())
        node_c  = Node_Id(Obj_Id())
        node_d  = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_b)                      # B has incoming from A
            _.index_edge(Edge_Id(Obj_Id()), node_b, node_c)                      # B has outgoing to C
            _.index_edge(Edge_Id(Obj_Id()), node_d, node_b)                      # B has incoming from D

            result = _.get_all_connected_nodes(node_b)

            assert node_a in result                                             # Incoming
            assert node_c in result                                             # Outgoing
            assert node_d in result                                             # Incoming
            assert len(result) == 3

    # =========================================================================
    # List-based Accessor Tests
    # =========================================================================

    def test_edges_ids__from__node_id(self):                                    # Test edges_ids__from__node_id
        node_id = Node_Id(Obj_Id())
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, node_id, Node_Id(Obj_Id()))

            result = _.edges_ids__from__node_id(node_id)

            assert isinstance(result, list)
            assert edge_id in result

    def test_edges_ids__to__node_id(self):                                      # Test edges_ids__to__node_id
        node_id = Node_Id(Obj_Id())
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, Node_Id(Obj_Id()), node_id)

            result = _.edges_ids__to__node_id(node_id)

            assert isinstance(result, list)
            assert edge_id in result

    def test_nodes_ids__from__node_id(self):                                    # Test nodes_ids__from__node_id
        node_a = Node_Id(Obj_Id())
        node_b = Node_Id(Obj_Id())
        node_c = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_b)
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_c)

            result = _.nodes_ids__from__node_id(node_a)

            assert isinstance(result, list)
            assert node_b in result
            assert node_c in result

    def test_nodes_ids__to__node_id(self):                                      # Test nodes_ids__to__node_id
        node_a = Node_Id(Obj_Id())
        node_b = Node_Id(Obj_Id())
        node_c = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_a, node_c)
            _.index_edge(Edge_Id(Obj_Id()), node_b, node_c)

            result = _.nodes_ids__to__node_id(node_c)

            assert isinstance(result, list)
            assert node_a in result
            assert node_b in result

    # =========================================================================
    # Raw Accessor Tests
    # =========================================================================

    def test_edges_to_nodes__accessor(self):                                    # Test raw accessor
        edge_id = Edge_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(edge_id, Node_Id(Obj_Id()), Node_Id(Obj_Id()))

            result = _.edges_to_nodes()

            assert edge_id in result

    def test_nodes_to_outgoing_edges__accessor(self):                           # Test raw accessor
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), node_id, Node_Id(Obj_Id()))

            result = _.nodes_to_outgoing_edges()

            assert node_id in result

    def test_nodes_to_incoming_edges__accessor(self):                           # Test raw accessor
        node_id = Node_Id(Obj_Id())

        with self.edges_index as _:
            _.index_edge(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), node_id)

            result = _.nodes_to_incoming_edges()

            assert node_id in result