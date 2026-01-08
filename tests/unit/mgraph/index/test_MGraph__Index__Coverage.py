from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats    import Schema__MGraph__Index__Stats
from osbot_utils.testing.Graph__Deterministic__Ids                  import graph_deterministic_ids
from osbot_utils.testing.Stdout                                     import Stdout
from osbot_utils.testing.Temp_File                                  import Temp_File
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.utils.Files                                        import file_exists
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from mgraph_db.mgraph.index.MGraph__Index                           import MGraph__Index
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label           import Schema__MGraph__Edge__Label
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path


class test_MGraph__Index__Coverage(TestCase):
    """Additional tests targeting uncovered code paths in MGraph__Index"""

    def setUp(self):
        self.mgraph_index = MGraph__Index()

    # =========================================================================
    # Print Methods Coverage
    # =========================================================================

    def test_print__index_data(self):                                           # Test print__index_data method
        with self.mgraph_index as _:
            with graph_deterministic_ids():
                node = Schema__MGraph__Node().set_node_type()
                _.add_node(node)

            with Stdout() as stdout:
                result = _.print__index_data()

            assert result is not None
            assert type(result) is dict
            assert result == _.index_data.json()
            assert stdout.value() == ('\n'
                                     "{ 'edges': { 'edges_to_nodes': {},\n"
                                     "             'nodes_to_incoming_edges': {'c0000001': []},\n"
                                     "             'nodes_to_outgoing_edges': {'c0000001': []}},\n"
                                     "  'labels': { 'edges_by_incoming_label': {},\n"
                                     "              'edges_by_outgoing_label': {},\n"
                                     "              'edges_by_predicate': {},\n"
                                     "              'edges_incoming_labels': {},\n"
                                     "              'edges_outgoing_labels': {},\n"
                                     "              'edges_predicates': {}},\n"
                                     "  'paths': {'edges_by_path': {}, 'nodes_by_path': {}},\n"
                                     "  'types': { 'edges_by_type': {},\n"
                                     "             'edges_types': {},\n"
                                     "             'nodes_by_type': {'Schema__MGraph__Node': ['c0000001']},\n"
                                     "             'nodes_to_incoming_edges_by_type': {},\n"
                                     "             'nodes_to_outgoing_edges_by_type': {},\n"
                                     "             'nodes_types': {'c0000001': 'Schema__MGraph__Node'}}}\n")


    def test_print__stats(self):                                                # Test print__stats method
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            with Stdout() as stdout:
                stats = _.print__stats()


            assert type(stats) is Schema__MGraph__Index__Stats

            assert stdout.value() == ('\n'
                                      "{ 'index_data': { 'edge_to_nodes': 0,\n"
                                      "                  'edges_by_path': {},\n"
                                      "                  'edges_by_type': {},\n"
                                      "                  'node_edge_connections': { 'avg_incoming_edges': 0,\n"
                                      "                                             'avg_outgoing_edges': 0,\n"
                                      "                                             'max_incoming_edges': 0,\n"
                                      "                                             'max_outgoing_edges': 0,\n"
                                      "                                             'total_nodes': 1},\n"
                                      "                  'nodes_by_path': {},\n"
                                      "                  'nodes_by_type': {'Schema__MGraph__Node': 1}},\n"
                                      "  'paths': {'edge_paths': {}, 'node_paths': {}},\n"
                                      "  'summary': { 'edges_with_paths': 0,\n"
                                      "               'nodes_with_paths': 0,\n"
                                      "               'total_edges': 0,\n"
                                      "               'total_nodes': 1,\n"
                                      "               'total_predicates': 0,\n"
                                      "               'unique_edge_paths': 0,\n"
                                      "               'unique_node_paths': 0}}\n")



    # =========================================================================
    # Remove Edge by ID Edge Cases
    # =========================================================================

    def test_remove_edge_by_id__without_type(self):                             # Test remove_edge_by_id when edge_type_name is None
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.types.edges_types[edge.edge_id]                          # Manually remove type to simulate edge case

            result = _.remove_edge_by_id(edge.edge_id)                          # Should still work without crashing

            assert result is _                                                  # Returns self for chaining
            assert edge.edge_id not in _.index_data.edges.edges_to_nodes

    def test_remove_edge_by_id__nonexistent_edge(self):                         # Test remove_edge_by_id with nonexistent edge
        with self.mgraph_index as _:
            fake_edge_id = Edge_Id(Obj_Id())

            result = _.remove_edge_by_id(fake_edge_id)                          # Should not crash

            assert result is _

    def test_remove_edge_by_id__edge_not_in_edges_to_nodes(self):               # Test when edge_id not in edges_to_nodes
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.edges.edges_to_nodes[edge.edge_id]                       # Remove from edges_to_nodes manually

            result = _.remove_edge_by_id(edge.edge_id)                          # Should handle gracefully

            assert result is _

    # =========================================================================
    # Remove Edge Path by ID Edge Cases
    # =========================================================================

    def test__remove_edge_path_by_id__edge_not_in_any_path(self):               # Test when edge has no path
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _._remove_edge_path_by_id(edge.edge_id)                             # Should not crash when no path exists

            assert edge.edge_id not in _.index_data.paths.edges_by_path               # Still empty

    def test__remove_edge_path_by_id__cleans_empty_set(self):                   # Test cleanup of empty path set
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id = node_1.node_id          ,
                                          to_node_id   = node_2.node_id          ,
                                          edge_path    = Edge_Path("solo.path")  )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert Edge_Path("solo.path") in _.index_data.paths.edges_by_path

            _._remove_edge_path_by_id(edge.edge_id)

            assert Edge_Path("solo.path") not in _.index_data.paths.edges_by_path     # Empty set should be cleaned up

    # =========================================================================
    # Remove Edge Node References Edge Cases
    # =========================================================================

    def test__remove_edge_node_references__missing_from_node(self):             # Test when from_node_id not in outgoing edges
        with self.mgraph_index as _:
            node_1    = Schema__MGraph__Node().set_node_type()
            node_2    = Schema__MGraph__Node().set_node_type()
            edge      = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_type = 'Schema__MGraph__Edge'

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.edges.nodes_to_outgoing_edges[node_1.node_id]            # Remove from_node from outgoing

            _.edges_index._remove_edge_from_node_sets(edge.edge_id, node_1.node_id, node_2.node_id)
            _.types_index.remove_edge_type_by_node(edge.edge_id, node_1.node_id, node_2.node_id, edge_type)

            assert True                                                         # Should not crash

    def test__remove_edge_node_references__missing_to_node(self):               # Test when to_node_id not in incoming edges
        with self.mgraph_index as _:
            node_1    = Schema__MGraph__Node().set_node_type()
            node_2    = Schema__MGraph__Node().set_node_type()
            edge      = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_type = 'Schema__MGraph__Edge'

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.edges.nodes_to_incoming_edges[node_2.node_id]            # Remove to_node from incoming

            _.edges_index._remove_edge_from_node_sets(edge.edge_id, node_1.node_id, node_2.node_id)
            _.types_index.remove_edge_type_by_node(edge.edge_id, node_1.node_id, node_2.node_id, edge_type)

            assert True                                                         # Should not crash

    def test__remove_edge_node_references__none_edge_type(self):                # Test with None edge_type_name
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _.edges_index._remove_edge_from_node_sets(edge.edge_id, node_1.node_id, node_2.node_id)
            _.types_index.remove_edge_type_by_node(edge.edge_id, node_1.node_id, node_2.node_id, None)

            assert True                                                         # Should handle None edge_type gracefully


    # =========================================================================
    # Remove Edge Type Reference Edge Cases
    # =========================================================================

    def test__remove_edge_type_reference__none_type(self):                      # Test with None edge_type_name
        with self.mgraph_index as _:
            _.types_index.remove_edge_type(Edge_Id(Obj_Id()), None)

            assert True                                                         # Should not crash

    def test__remove_edge_type_reference__type_not_in_index(self):              # Test when type not in edges_by_type
        with self.mgraph_index as _:
            _.types_index.remove_edge_type(Edge_Id(Obj_Id()), 'NonExistentType')

            assert True                                                         # Should not crash

    def test__remove_edge_type_reference__cleans_empty_set(self):               # Test cleanup of empty type set
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            edge_type = 'Schema__MGraph__Edge'
            assert edge_type in _.index_data.types.edges_by_type

            _.types_index.remove_edge_type(edge.edge_id, edge_type)

            assert edge_type not in _.index_data.types.edges_by_type                  # Empty set should be cleaned

    # =========================================================================
    # Remove Edge Label by ID Edge Cases
    # =========================================================================

    def test__remove_edge_label_by_id__no_labels(self):                         # Test when edge has no labels
        with self.mgraph_index as _:
            _._remove_edge_label_by_id(Edge_Id(Obj_Id()))

            assert True                                                         # Should not crash

    def test__remove_edge_label_by_id__partial_labels(self):                    # Test when edge has only some labels
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('only_pred'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert Safe_Id('only_pred') in _.index_data.labels.edges_by_predicate

            _._remove_edge_label_by_id(edge.edge_id)

            assert Safe_Id('only_pred') not in _.index_data.labels.edges_by_predicate

    def test__remove_edge_label_by_id__all_label_types(self):                   # Test removal of all label types
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate = Safe_Id('pred'    ),
                                                     incoming  = Safe_Id('incoming'),
                                                     outgoing  = Safe_Id('outgoing'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _._remove_edge_label_by_id(edge.edge_id)

            assert Safe_Id('pred'    ) not in _.index_data.labels.edges_by_predicate
            assert Safe_Id('incoming') not in _.index_data.labels.edges_by_incoming_label
            assert Safe_Id('outgoing') not in _.index_data.labels.edges_by_outgoing_label

    # =========================================================================
    # Remove Edge Label (Standalone Method)
    # =========================================================================

    def test_remove_edge_label__with_all_labels(self):                          # Test remove_edge_label method directly
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate = Safe_Id('to_remove'         ),
                                                     incoming  = Safe_Id('incoming_to_remove'),
                                                     outgoing  = Safe_Id('outgoing_to_remove'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _.remove_edge_label(edge)                                           # Use standalone method

            assert Safe_Id('to_remove'         ) not in _.index_data.labels.edges_by_predicate
            assert Safe_Id('incoming_to_remove') not in _.index_data.labels.edges_by_incoming_label
            assert Safe_Id('outgoing_to_remove') not in _.index_data.labels.edges_by_outgoing_label
            assert edge.edge_id                   not in _.index_data.labels.edges_predicates

    def test_remove_edge_label__no_label(self):                                 # Test remove_edge_label with edge without label
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _.remove_edge_label(edge)                                           # Should not crash

            assert True

    def test_remove_edge_label__only_predicate(self):                           # Test with only predicate label
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('just_pred'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _.remove_edge_label(edge)

            assert Safe_Id('just_pred') not in _.index_data.labels.edges_by_predicate

    def test_remove_edge_label__predicate_not_in_index(self):                   # Test when predicate already removed from index
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('orphan_pred'))
            edge       = Schema__MGraph__Edge(from_node_id = node_1.node_id ,
                                              to_node_id   = node_2.node_id ,
                                              edge_label   = edge_label     )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.labels.edges_by_predicate[Safe_Id('orphan_pred')]         # Manually remove

            _.remove_edge_label(edge)                                           # Should not crash

            assert True

    # =========================================================================
    # Remove Edge Path (Standalone Method)
    # =========================================================================

    def test_remove_edge_path__with_path(self):                                 # Test remove_edge_path method
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id = node_1.node_id          ,
                                          to_node_id   = node_2.node_id          ,
                                          edge_path    = Edge_Path("to.remove")  )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            assert Edge_Path("to.remove") in _.index_data.paths.edges_by_path

            _.remove_edge_path(edge)

            assert Edge_Path("to.remove") not in _.index_data.paths.edges_by_path

    def test_remove_edge_path__no_path(self):                                   # Test remove_edge_path with no path
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            _.remove_edge_path(edge)                                            # Should not crash

            assert True

    def test_remove_edge_path__path_not_in_index(self):                         # Test when path already removed
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id = node_1.node_id            ,
                                          to_node_id   = node_2.node_id            ,
                                          edge_path    = Edge_Path("orphan.path")  )

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            del _.index_data.paths.edges_by_path[Edge_Path("orphan.path")]            # Manually remove

            _.remove_edge_path(edge)                                            # Should not crash

            assert True

    # =========================================================================
    # Remove Node with Connected Edges
    # =========================================================================

    def test_remove_node__with_outgoing_edges(self):                            # Test node removal cleans up outgoing edges
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_3.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            _.remove_node(node_1)                                               # Remove node with outgoing edges

            assert node_1.node_id not in _.index_data.edges.nodes_to_outgoing_edges
            assert edge_1.edge_id not in _.index_data.edges.edges_to_nodes
            assert edge_2.edge_id not in _.index_data.edges.edges_to_nodes

    def test_remove_node__with_incoming_edges(self):                            # Test node removal cleans up incoming edges
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            node_3 = Schema__MGraph__Node().set_node_type()

            edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_3.node_id)
            edge_2 = Schema__MGraph__Edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_node(node_3)
            _.add_edge(edge_1)
            _.add_edge(edge_2)

            _.remove_node(node_3)                                               # Remove node with incoming edges

            assert node_3.node_id not in _.index_data.edges.nodes_to_incoming_edges
            assert edge_1.edge_id not in _.index_data.edges.edges_to_nodes
            assert edge_2.edge_id not in _.index_data.edges.edges_to_nodes

    def test_remove_node__cleans_type_index(self):                              # Test type index cleanup
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            assert 'Schema__MGraph__Node' in _.index_data.types.nodes_by_type

            _.remove_node(node)

            assert 'Schema__MGraph__Node' not in _.index_data.types.nodes_by_type     # Type entry removed when empty

    # =========================================================================
    # Get Node Edges Methods
    # =========================================================================

    def test_get_node_outgoing_edges__with_edges(self):                         # Test get_node_outgoing_edges
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_node_outgoing_edges(node_1)

            assert edge.edge_id in result

    def test_get_node_outgoing_edges__no_edges(self):                           # Test with node having no outgoing edges
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.get_node_outgoing_edges(node)

            assert result == set()

    def test_get_node_incoming_edges__with_edges(self):                         # Test get_node_incoming_edges
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            result = _.get_node_incoming_edges(node_2)

            assert edge.edge_id in result

    def test_get_node_incoming_edges__no_edges(self):                           # Test with node having no incoming edges
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.get_node_incoming_edges(node)

            assert result == set()

    # =========================================================================
    # Edges IDs Methods Edge Cases
    # =========================================================================

    def test_edges_ids__from__node_id__empty(self):                             # Test with node having no outgoing edges
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.edges_ids__from__node_id(node.node_id)

            assert result == []

    def test_edges_ids__to__node_id__empty(self):                               # Test with node having no incoming edges
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.edges_ids__to__node_id(node.node_id)

            assert result == []

    def test_edges_ids__from__node_id__nonexistent(self):                       # Test with nonexistent node_id
        with self.mgraph_index as _:
            result = _.edges_ids__from__node_id(Node_Id(Obj_Id()))

            assert result == []

    def test_nodes_ids__from__node_id__empty(self):                             # Test with node having no connections
        with self.mgraph_index as _:
            node = Schema__MGraph__Node().set_node_type()
            _.add_node(node)

            result = _.nodes_ids__from__node_id(node.node_id)

            assert result == []

    # =========================================================================
    # File Operations
    # =========================================================================

    def test_save_to_file__and_from_file(self):                                 # Test save and load roundtrip
        with self.mgraph_index as _:
            node_1 = Schema__MGraph__Node().set_node_type()
            node_2 = Schema__MGraph__Node().set_node_type()
            edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            with Temp_File(return_file_path=True, extension='json', create_file=False) as target_file:
                _.save_to_file(target_file)
                assert file_exists(target_file)

                loaded_index = MGraph__Index.from_file(target_file)
                assert len(loaded_index.index_data.edges.edges_to_nodes) == 1
                assert len(loaded_index.nodes_by_type()                )  == 1
                assert _.json()                                    == loaded_index.json()
                assert _.obj ()                                    == loaded_index.obj()

    # =========================================================================
    # Value Node Operations in Index
    # =========================================================================

    def test_add_node__with_value_node(self):                                   # Test adding value node to main index
        with self.mgraph_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="test", value_type=str)
            value_node.node_type = Schema__MGraph__Node__Value

            _.add_node(value_node)

            assert value_node.node_id in _.index_data.types.nodes_types
            assert value_node.node_id in _.values_index.index_data.node_to_hash

    def test_remove_node__with_value_node(self):                                # Test removing value node from main index
        with self.mgraph_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="to_remove", value_type=str)
            value_node.node_type = Schema__MGraph__Node__Value

            _.add_node(value_node)

            hash_before = _.values_index.index_data.node_to_hash.get(value_node.node_id)
            assert hash_before is not None

            _.remove_node(value_node)

            assert value_node.node_id not in _.values_index.index_data.node_to_hash

    # =========================================================================
    # Raw Data Accessors
    # =========================================================================

    def test_nodes_to_incoming_edges_by_type__accessor(self):                   # Test raw accessor
        with self.mgraph_index as _:
            result = _.nodes_to_incoming_edges_by_type()

            assert result == {}

    def test_nodes_to_outgoing_edges_by_type__accessor(self):                   # Test raw accessor
        with self.mgraph_index as _:
            result = _.nodes_to_outgoing_edges_by_type()

            assert result == {}

    def test_edges_by_type__accessor(self):                                     # Test raw accessor
        with self.mgraph_index as _:
            result = _.edges_by_type()

            assert result == {}