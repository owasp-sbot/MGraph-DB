from unittest                                                       import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Types                    import MGraph__Index__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Types   import Schema__MGraph__Index__Data__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class test_MGraph__Index__Types(TestCase):

    def setUp(self):
        self.types_data  = Schema__MGraph__Index__Data__Types()
        self.types_index = MGraph__Index__Types(data=self.types_data)

    def test__init__(self):                                                     # Test initialization
        with self.types_index as _:
            assert type(_)            is MGraph__Index__Types
            assert type(_.data) is Schema__MGraph__Index__Data__Types
            assert _.nodes_types()    == {}
            assert _.nodes_by_type()  == {}
            assert _.edges_types()    == {}
            assert _.edges_by_type()  == {}
            assert _.nodes_to_incoming_edges_by_type() == {}
            assert _.nodes_to_outgoing_edges_by_type() == {}

    # =========================================================================
    # Node Type - Add Tests
    # =========================================================================

    def test_index_node_type(self):                                             # Test indexing node type
        node_id   = Node_Id(Obj_Id())
        type_name = 'Schema__MGraph__Node'

        with self.types_index as _:
            _.index_node_type(node_id, type_name)

            assert node_id   in _.nodes_types()
            assert _.nodes_types()[node_id] == type_name
            assert type_name in _.nodes_by_type()
            assert node_id   in _.nodes_by_type()[type_name]

    def test_index_node_type__multiple_same_type(self):                         # Test multiple nodes with same type
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())
        type_name = 'Schema__MGraph__Node'

        with self.types_index as _:
            _.index_node_type(node_id_1, type_name)
            _.index_node_type(node_id_2, type_name)

            assert len(_.nodes_by_type()[type_name]) == 2
            assert node_id_1 in _.nodes_by_type()[type_name]
            assert node_id_2 in _.nodes_by_type()[type_name]

    def test_index_node_type__multiple_different_types(self):                   # Test nodes with different types
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_node_type(node_id_1, 'TypeA')
            _.index_node_type(node_id_2, 'TypeB')

            assert 'TypeA' in _.nodes_by_type()
            assert 'TypeB' in _.nodes_by_type()
            assert node_id_1 in _.nodes_by_type()['TypeA']
            assert node_id_2 in _.nodes_by_type()['TypeB']

    # =========================================================================
    # Node Type - Remove Tests
    # =========================================================================

    def test_remove_node_type(self):                                            # Test removing node type
        node_id   = Node_Id(Obj_Id())
        type_name = 'Schema__MGraph__Node'

        with self.types_index as _:
            _.index_node_type(node_id, type_name)
            _.remove_node_type(node_id, type_name)

            assert node_id   not in _.nodes_types()
            assert type_name not in _.nodes_by_type()                           # Empty set cleaned up

    def test_remove_node_type__keeps_other_nodes(self):                         # Test removing one node keeps others
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())
        type_name = 'Schema__MGraph__Node'

        with self.types_index as _:
            _.index_node_type(node_id_1, type_name)
            _.index_node_type(node_id_2, type_name)
            _.remove_node_type(node_id_1, type_name)

            assert type_name     in _.nodes_by_type()
            assert node_id_1 not in _.nodes_by_type()[type_name]
            assert node_id_2     in _.nodes_by_type()[type_name]

    def test_remove_node_type__nonexistent(self):                               # Test removing nonexistent node type
        with self.types_index as _:
            _.remove_node_type(Node_Id(Obj_Id()), 'NonExistent')                        # Should not crash

            assert True

    # =========================================================================
    # Edge Type - Add Tests
    # =========================================================================

    def test_index_edge_type(self):                                             # Test indexing edge type
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'Schema__MGraph__Edge'

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, type_name)

            assert edge_id   in _.edges_types()
            assert _.edges_types()[edge_id] == type_name
            assert type_name in _.edges_by_type()
            assert edge_id   in _.edges_by_type()[type_name]

            # Check node-edge type mappings
            assert from_node_id in _.nodes_to_outgoing_edges_by_type()
            assert type_name    in _.nodes_to_outgoing_edges_by_type()[from_node_id]
            assert edge_id      in _.nodes_to_outgoing_edges_by_type()[from_node_id][type_name]

            assert to_node_id in _.nodes_to_incoming_edges_by_type()
            assert type_name  in _.nodes_to_incoming_edges_by_type()[to_node_id]
            assert edge_id    in _.nodes_to_incoming_edges_by_type()[to_node_id][type_name]

    def test_index_edge_type__multiple_same_type(self):                         # Test multiple edges with same type
        edge_id_1    = Edge_Id(Obj_Id())
        edge_id_2    = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'Schema__MGraph__Edge'

        with self.types_index as _:
            _.index_edge_type(edge_id_1, from_node_id, to_node_id, type_name)
            _.index_edge_type(edge_id_2, from_node_id, to_node_id, type_name)

            assert len(_.edges_by_type()[type_name]) == 2
            assert edge_id_1 in _.edges_by_type()[type_name]
            assert edge_id_2 in _.edges_by_type()[type_name]

    # =========================================================================
    # Edge Type - Remove Tests
    # =========================================================================

    def test_remove_edge_type(self):                                            # Test removing edge type from edges_by_type
        edge_id   = Edge_Id(Obj_Id())
        type_name = 'Schema__MGraph__Edge'

        with self.types_index as _:
            # Manually add to edges_by_type
            _.edges_by_type()[type_name] = {edge_id}

            _.remove_edge_type(edge_id, type_name)

            assert type_name not in _.edges_by_type()                           # Empty set cleaned up

    def test_remove_edge_type__keeps_other_edges(self):                         # Test removing one edge keeps others
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        type_name = 'Schema__MGraph__Edge'

        with self.types_index as _:
            _.edges_by_type()[type_name] = {edge_id_1, edge_id_2}

            _.remove_edge_type(edge_id_1, type_name)

            assert type_name     in _.edges_by_type()
            assert edge_id_1 not in _.edges_by_type()[type_name]
            assert edge_id_2     in _.edges_by_type()[type_name]

    def test_remove_edge_type__none_type(self):                                 # Test with None type name
        with self.types_index as _:
            _.remove_edge_type(Edge_Id(Obj_Id()), None)                                 # Should not crash

            assert True

    def test_remove_edge_type_by_node(self):                                    # Test removing edge type from node mappings
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'Schema__MGraph__Edge'

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, type_name)
            _.remove_edge_type_by_node(edge_id, from_node_id, to_node_id, type_name)

            # Node mappings should be cleaned up
            assert from_node_id not in _.nodes_to_outgoing_edges_by_type()
            assert to_node_id   not in _.nodes_to_incoming_edges_by_type()

    def test_remove_edge_type_by_node__keeps_other_edges(self):                 # Test keeps other edges
        edge_id_1    = Edge_Id(Obj_Id())
        edge_id_2    = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'Schema__MGraph__Edge'

        with self.types_index as _:
            _.index_edge_type(edge_id_1, from_node_id, to_node_id, type_name)
            _.index_edge_type(edge_id_2, from_node_id, to_node_id, type_name)
            _.remove_edge_type_by_node(edge_id_1, from_node_id, to_node_id, type_name)

            assert from_node_id     in _.nodes_to_outgoing_edges_by_type()
            assert edge_id_1    not in _.nodes_to_outgoing_edges_by_type()[from_node_id][type_name]
            assert edge_id_2        in _.nodes_to_outgoing_edges_by_type()[from_node_id][type_name]

    # =========================================================================
    # Node Type - Query Tests
    # =========================================================================

    def test_get_node_type__found(self):                                        # Test get_node_type
        node_id   = Node_Id(Obj_Id())
        type_name = 'MyNodeType'

        with self.types_index as _:
            _.index_node_type(node_id, type_name)

            result = _.get_node_type(node_id)

            assert result == type_name

    def test_get_node_type__not_found(self):                                    # Test get_node_type with nonexistent node
        with self.types_index as _:
            result = _.get_node_type(Node_Id(Obj_Id()))

            assert result is None

    def test_get_nodes_by_type(self):                                           # Test get_nodes_by_type
        node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_node_type(node_id, 'Schema__MGraph__Node')

            result = _.get_nodes_by_type(Schema__MGraph__Node)

            assert node_id in result

    def test_get_nodes_by_type_name(self):                                      # Test get_nodes_by_type_name
        node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_node_type(node_id, 'MyType')

            result = _.get_nodes_by_type_name('MyType')

            assert node_id in result

    def test_get_nodes_by_type_name__not_found(self):                           # Test with nonexistent type
        with self.types_index as _:
            result = _.get_nodes_by_type_name('NonExistent')

            assert result == set()

    def test_get_all_node_types(self):                                          # Test get_all_node_types
        with self.types_index as _:
            _.index_node_type(Node_Id(Obj_Id()), 'TypeA')
            _.index_node_type(Node_Id(Obj_Id()), 'TypeB')
            _.index_node_type(Node_Id(Obj_Id()), 'TypeC')

            result = _.get_all_node_types()

            assert 'TypeA' in result
            assert 'TypeB' in result
            assert 'TypeC' in result
            assert len(result) == 3

    def test_has_node_type(self):                                               # Test has_node_type
        with self.types_index as _:
            _.index_node_type(Node_Id(Obj_Id()), 'ExistingType')

            assert _.has_node_type('ExistingType') is True
            assert _.has_node_type('NonExistent')  is False

    def test_count_nodes_by_type(self):                                         # Test count_nodes_by_type
        with self.types_index as _:
            _.index_node_type(Node_Id(Obj_Id()), 'CountedType')
            _.index_node_type(Node_Id(Obj_Id()), 'CountedType')
            _.index_node_type(Node_Id(Obj_Id()), 'CountedType')

            assert _.count_nodes_by_type('CountedType') == 3
            assert _.count_nodes_by_type('NonExistent') == 0

    # =========================================================================
    # Edge Type - Query Tests
    # =========================================================================

    def test_get_edge_type__found(self):                                        # Test get_edge_type
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'MyEdgeType'

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, type_name)

            result = _.get_edge_type(edge_id)

            assert result == type_name

    def test_get_edge_type__not_found(self):                                    # Test get_edge_type with nonexistent edge
        with self.types_index as _:
            result = _.get_edge_type(Edge_Id(Obj_Id()))

            assert result is None

    def test_get_edges_by_type(self):                                           # Test get_edges_by_type
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, 'Schema__MGraph__Edge')

            result = _.get_edges_by_type(Schema__MGraph__Edge)

            assert edge_id in result

    def test_get_edges_by_type_name(self):                                      # Test get_edges_by_type_name
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, 'MyEdge')

            result = _.get_edges_by_type_name('MyEdge')

            assert edge_id in result

    def test_get_all_edge_types(self):                                          # Test get_all_edge_types
        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'EdgeTypeA')
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'EdgeTypeB')

            result = _.get_all_edge_types()

            assert 'EdgeTypeA' in result
            assert 'EdgeTypeB' in result

    def test_has_edge_type(self):                                               # Test has_edge_type
        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'ExistingEdge')

            assert _.has_edge_type('ExistingEdge') is True
            assert _.has_edge_type('NonExistent')  is False

    def test_count_edges_by_type(self):                                         # Test count_edges_by_type
        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'CountedEdge')
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'CountedEdge')

            assert _.count_edges_by_type('CountedEdge') == 2
            assert _.count_edges_by_type('NonExistent') == 0

    # =========================================================================
    # Node-Edge Type Query Tests
    # =========================================================================

    def test_get_node_incoming_edges_by_type(self):                             # Test get_node_incoming_edges_by_type
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'IncomingEdge'

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, type_name)

            result = _.get_node_incoming_edges_by_type(to_node_id, type_name)

            assert edge_id in result

    def test_get_node_incoming_edges_by_type__not_found(self):                  # Test with nonexistent
        with self.types_index as _:
            result = _.get_node_incoming_edges_by_type(Node_Id(Obj_Id()), 'NonExistent')

            assert result == set()

    def test_get_node_outgoing_edges_by_type(self):                             # Test get_node_outgoing_edges_by_type
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        type_name    = 'OutgoingEdge'

        with self.types_index as _:
            _.index_edge_type(edge_id, from_node_id, to_node_id, type_name)

            result = _.get_node_outgoing_edges_by_type(from_node_id, type_name)

            assert edge_id in result

    def test_get_node_edge_types_incoming(self):                                # Test get_node_edge_types_incoming
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), from_node_id, to_node_id, 'TypeA')
            _.index_edge_type(Edge_Id(Obj_Id()), from_node_id, to_node_id, 'TypeB')

            result = _.get_node_edge_types_incoming(to_node_id)

            assert 'TypeA' in result
            assert 'TypeB' in result

    def test_get_node_edge_types_outgoing(self):                                # Test get_node_edge_types_outgoing
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), from_node_id, to_node_id, 'TypeX')
            _.index_edge_type(Edge_Id(Obj_Id()), from_node_id, to_node_id, 'TypeY')

            result = _.get_node_edge_types_outgoing(from_node_id)

            assert 'TypeX' in result
            assert 'TypeY' in result

    # =========================================================================
    # Raw Accessor Tests
    # =========================================================================

    def test_nodes_types__accessor(self):                                       # Test raw accessor
        node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_node_type(node_id, 'TestType')

            result = _.nodes_types()

            assert node_id in result

    def test_nodes_by_type__accessor(self):                                     # Test raw accessor
        node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_node_type(node_id, 'TestType')

            result = _.nodes_by_type()

            assert 'TestType' in result

    def test_edges_types__accessor(self):                                       # Test raw accessor
        edge_id = Edge_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(edge_id, Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'EdgeType')

            result = _.edges_types()

            assert edge_id in result

    def test_edges_by_type__accessor(self):                                     # Test raw accessor
        edge_id = Edge_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(edge_id, Node_Id(Obj_Id()), Node_Id(Obj_Id()), 'EdgeType')

            result = _.edges_by_type()

            assert 'EdgeType' in result

    def test_nodes_to_incoming_edges_by_type__accessor(self):                   # Test raw accessor
        to_node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), Node_Id(Obj_Id()), to_node_id, 'EdgeType')

            result = _.nodes_to_incoming_edges_by_type()

            assert to_node_id in result

    def test_nodes_to_outgoing_edges_by_type__accessor(self):                   # Test raw accessor
        from_node_id = Node_Id(Obj_Id())

        with self.types_index as _:
            _.index_edge_type(Edge_Id(Obj_Id()), from_node_id, Node_Id(Obj_Id()), 'EdgeType')

            result = _.nodes_to_outgoing_edges_by_type()

            assert from_node_id in result