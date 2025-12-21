from unittest                                                       import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Labels                   import MGraph__Index__Labels
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label           import Schema__MGraph__Edge__Label
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels   import Schema__MGraph__Index__Data__Labels
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id


class test_MGraph__Index__Labels(TestCase):

    def setUp(self):
        self.labels_data  = Schema__MGraph__Index__Data__Labels()
        self.labels_index = MGraph__Index__Labels(data=self.labels_data)

    def test__init__(self):                                                     # Test initialization
        with self.labels_index as _:
            assert type(_)            is MGraph__Index__Labels
            assert type(_.data) is Schema__MGraph__Index__Data__Labels
            assert _.edges_predicates()       == {}
            assert _.edges_by_predicate()     == {}
            assert _.edges_incoming_labels()  == {}
            assert _.edges_by_incoming_label() == {}
            assert _.edges_outgoing_labels()  == {}
            assert _.edges_by_outgoing_label() == {}

    # =========================================================================
    # Add Edge Label Tests
    # =========================================================================

    def test_add_edge_label__with_predicate(self):                              # Test adding edge with predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('test_pred'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert edge.edge_id             in _.edges_predicates()
            assert _.edges_predicates()[edge.edge_id] == Safe_Id('test_pred')
            assert Safe_Id('test_pred')     in _.edges_by_predicate()
            assert edge.edge_id             in _.edges_by_predicate()[Safe_Id('test_pred')]

    def test_add_edge_label__with_incoming(self):                               # Test adding edge with incoming label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(incoming=Safe_Id('incoming_label'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert edge.edge_id                  in _.edges_incoming_labels()
            assert _.edges_incoming_labels()[edge.edge_id] == Safe_Id('incoming_label')
            assert Safe_Id('incoming_label')     in _.edges_by_incoming_label()
            assert edge.edge_id                  in _.edges_by_incoming_label()[Safe_Id('incoming_label')]

    def test_add_edge_label__with_outgoing(self):                               # Test adding edge with outgoing label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(outgoing=Safe_Id('outgoing_label'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert edge.edge_id                  in _.edges_outgoing_labels()
            assert _.edges_outgoing_labels()[edge.edge_id] == Safe_Id('outgoing_label')
            assert Safe_Id('outgoing_label')     in _.edges_by_outgoing_label()
            assert edge.edge_id                  in _.edges_by_outgoing_label()[Safe_Id('outgoing_label')]

    def test_add_edge_label__with_all_labels(self):                             # Test adding edge with all label types
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate = Safe_Id('pred'    ),
                                            incoming  = Safe_Id('incoming'),
                                            outgoing  = Safe_Id('outgoing'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert Safe_Id('pred'    ) in _.edges_by_predicate()
            assert Safe_Id('incoming') in _.edges_by_incoming_label()
            assert Safe_Id('outgoing') in _.edges_by_outgoing_label()

    def test_add_edge_label__without_label(self):                               # Test adding edge without any label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        with self.labels_index as _:
            _.add_edge_label(edge)                                              # Should not crash

            assert _.edges_predicates()        == {}
            assert _.edges_by_predicate()      == {}
            assert _.edges_incoming_labels()   == {}
            assert _.edges_by_incoming_label() == {}

    def test_add_edge_label__multiple_edges_same_predicate(self):               # Test multiple edges with same predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        node3 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(predicate=Safe_Id('shared'))
        label2 = Schema__MGraph__Edge__Label(predicate=Safe_Id('shared'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node2.node_id, to_node_id=node3.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            assert len(_.edges_by_predicate()[Safe_Id('shared')]) == 2
            assert edge1.edge_id in _.edges_by_predicate()[Safe_Id('shared')]
            assert edge2.edge_id in _.edges_by_predicate()[Safe_Id('shared')]

    # =========================================================================
    # Remove Edge Label Tests
    # =========================================================================

    def test_remove_edge_label__with_all_labels(self):                          # Test removing edge with all labels
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate = Safe_Id('pred'    ),
                                            incoming  = Safe_Id('incoming'),
                                            outgoing  = Safe_Id('outgoing'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)
            _.remove_edge_label(edge)

            assert Safe_Id('pred'    ) not in _.edges_by_predicate()
            assert Safe_Id('incoming') not in _.edges_by_incoming_label()
            assert Safe_Id('outgoing') not in _.edges_by_outgoing_label()
            assert edge.edge_id        not in _.edges_predicates()

    def test_remove_edge_label__without_label(self):                            # Test removing edge without label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        with self.labels_index as _:
            _.remove_edge_label(edge)                                           # Should not crash

            assert True

    def test_remove_edge_label__keeps_other_edges(self):                        # Test removing one edge keeps others
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        node3 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(predicate=Safe_Id('shared'))
        label2 = Schema__MGraph__Edge__Label(predicate=Safe_Id('shared'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node2.node_id, to_node_id=node3.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)
            _.remove_edge_label(edge1)

            assert Safe_Id('shared') in _.edges_by_predicate()
            assert edge1.edge_id not in _.edges_by_predicate()[Safe_Id('shared')]
            assert edge2.edge_id     in _.edges_by_predicate()[Safe_Id('shared')]

    def test_remove_edge_label_by_id__found(self):                              # Test removing edge label by ID
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate = Safe_Id('pred'    ),
                                            incoming  = Safe_Id('incoming'),
                                            outgoing  = Safe_Id('outgoing'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)
            _.remove_edge_label_by_id(edge.edge_id)

            assert Safe_Id('pred'    ) not in _.edges_by_predicate()
            assert Safe_Id('incoming') not in _.edges_by_incoming_label()
            assert Safe_Id('outgoing') not in _.edges_by_outgoing_label()

    def test_remove_edge_label_by_id__not_found(self):                          # Test removing nonexistent edge label
        with self.labels_index as _:
            _.remove_edge_label_by_id(Edge_Id(Obj_Id()))                                # Should not crash

            assert True

    # =========================================================================
    # Query Tests
    # =========================================================================

    def test_get_edge_predicate__found(self):                                   # Test get_edge_predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('my_pred'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.get_edge_predicate(edge.edge_id)

            assert result == Safe_Id('my_pred')

    def test_get_edge_predicate__not_found(self):                               # Test get_edge_predicate with nonexistent edge
        with self.labels_index as _:
            result = _.get_edge_predicate(Edge_Id(Obj_Id()))

            assert result is None

    def test_get_edges_by_predicate__found(self):                               # Test get_edges_by_predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('query_pred'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.get_edges_by_predicate(Safe_Id('query_pred'))

            assert edge.edge_id in result

    def test_get_edges_by_predicate__not_found(self):                           # Test get_edges_by_predicate with nonexistent predicate
        with self.labels_index as _:
            result = _.get_edges_by_predicate(Safe_Id('nonexistent'))

            assert result == set()

    def test_get_edges_by_incoming_label__found(self):                          # Test get_edges_by_incoming_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(incoming=Safe_Id('incoming_query'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.get_edges_by_incoming_label(Safe_Id('incoming_query'))

            assert edge.edge_id in result

    def test_get_edges_by_outgoing_label__found(self):                          # Test get_edges_by_outgoing_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(outgoing=Safe_Id('outgoing_query'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.get_edges_by_outgoing_label(Safe_Id('outgoing_query'))

            assert edge.edge_id in result

    def test_get_all_predicates(self):                                          # Test get_all_predicates
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(predicate=Safe_Id('pred1'))
        label2 = Schema__MGraph__Edge__Label(predicate=Safe_Id('pred2'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            result = _.get_all_predicates()

            assert Safe_Id('pred1') in result
            assert Safe_Id('pred2') in result
            assert len(result) == 2

    def test_get_all_incoming_labels(self):                                     # Test get_all_incoming_labels
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(incoming=Safe_Id('in1'))
        label2 = Schema__MGraph__Edge__Label(incoming=Safe_Id('in2'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            result = _.get_all_incoming_labels()

            assert Safe_Id('in1') in result
            assert Safe_Id('in2') in result

    def test_get_all_outgoing_labels(self):                                     # Test get_all_outgoing_labels
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(outgoing=Safe_Id('out1'))
        label2 = Schema__MGraph__Edge__Label(outgoing=Safe_Id('out2'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            result = _.get_all_outgoing_labels()

            assert Safe_Id('out1') in result
            assert Safe_Id('out2') in result

    def test_has_predicate(self):                                               # Test has_predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('exists'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert _.has_predicate(Safe_Id('exists'))     is True
            assert _.has_predicate(Safe_Id('not_exists')) is False

    def test_has_incoming_label(self):                                          # Test has_incoming_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(incoming=Safe_Id('exists'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert _.has_incoming_label(Safe_Id('exists'))     is True
            assert _.has_incoming_label(Safe_Id('not_exists')) is False

    def test_has_outgoing_label(self):                                          # Test has_outgoing_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(outgoing=Safe_Id('exists'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            assert _.has_outgoing_label(Safe_Id('exists'))     is True
            assert _.has_outgoing_label(Safe_Id('not_exists')) is False

    def test_count_edges_by_predicate(self):                                    # Test count_edges_by_predicate
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        node3 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(predicate=Safe_Id('counted'))
        label2 = Schema__MGraph__Edge__Label(predicate=Safe_Id('counted'))
        label3 = Schema__MGraph__Edge__Label(predicate=Safe_Id('counted'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node2.node_id, to_node_id=node3.node_id, edge_label=label2)
        edge3 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node3.node_id, edge_label=label3)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)
            _.add_edge_label(edge3)

            assert _.count_edges_by_predicate(Safe_Id('counted'))     == 3
            assert _.count_edges_by_predicate(Safe_Id('nonexistent')) == 0

    def test_count_edges_by_incoming_label(self):                               # Test count_edges_by_incoming_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(incoming=Safe_Id('counted'))
        label2 = Schema__MGraph__Edge__Label(incoming=Safe_Id('counted'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            assert _.count_edges_by_incoming_label(Safe_Id('counted'))     == 2
            assert _.count_edges_by_incoming_label(Safe_Id('nonexistent')) == 0

    def test_count_edges_by_outgoing_label(self):                               # Test count_edges_by_outgoing_label
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label1 = Schema__MGraph__Edge__Label(outgoing=Safe_Id('counted'))
        label2 = Schema__MGraph__Edge__Label(outgoing=Safe_Id('counted'))
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label1)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label2)

        with self.labels_index as _:
            _.add_edge_label(edge1)
            _.add_edge_label(edge2)

            assert _.count_edges_by_outgoing_label(Safe_Id('counted'))     == 2
            assert _.count_edges_by_outgoing_label(Safe_Id('nonexistent')) == 0

    # =========================================================================
    # Raw Accessor Tests
    # =========================================================================

    def test_edges_predicates__accessor(self):                                  # Test raw accessor
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('accessor'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.edges_predicates()

            assert edge.edge_id in result

    def test_edges_by_predicate__accessor(self):                                # Test raw accessor
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        label = Schema__MGraph__Edge__Label(predicate=Safe_Id('accessor'))
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_label=label)

        with self.labels_index as _:
            _.add_edge_label(edge)

            result = _.edges_by_predicate()

            assert Safe_Id('accessor') in result

    def test_edges_incoming_labels__accessor(self):                             # Test raw accessor
        with self.labels_index as _:
            result = _.edges_incoming_labels()

            assert result == {}

    def test_edges_outgoing_labels__accessor(self):                             # Test raw accessor
        with self.labels_index as _:
            result = _.edges_outgoing_labels()

            assert result == {}