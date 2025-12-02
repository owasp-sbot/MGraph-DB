from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.utils.MGraph__Random_Graph                    import create_empty_mgraph


class test_MGraph__path_mode(TestCase):

    def test_path_mode_graph_creation(self):                                                # Create graph without explicit types
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            node = _.new_value("hello", node_path=Node_Path("root"))

            # Should work without types
            assert node.node_data.value == "hello"
            assert node.node.data.node_path == "root"

    def test__bug__path_mode_serialization_minimal(self):                                         # Verify path-mode graphs serialize without type overhead
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            _.new_value("test")

        json_data = mgraph.graph.model.data.json__compress()

        # These should not be present or be None (omitted)
        #assert json_data.get('graph_type' ) is None or 'graph_type'  not in json_data
        #assert json_data.get('schema_types') is None or 'schema_types' not in json_data

        assert json_data.get('graph_type' ) == '@schema_mgraph_graph'                       # BUG: these should not be here
        assert json_data.get('schema_types') == { 'edge_type': None,
                                                  'graph_data_type': None,
                                                  'node_data_type': None,
                                                  'node_type': None}

    def test_path_mode_multiple_nodes(self):                                                # Create multiple nodes in path-mode
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            node1 = _.new_value("first" , node_path=Node_Path("root.first" ))
            node2 = _.new_value("second", node_path=Node_Path("root.second"))
            node3 = _.new_value("third" , node_path=Node_Path("root.third" ))

            edge = _.connect_nodes(node1, node2)

        with mgraph.data() as _:
            assert len(_.nodes()) == 3
            assert len(_.edges()) == 1

    def test_path_mode_with_predicates(self):                                               # Use predicates in path-mode
        mgraph = create_empty_mgraph()

        with mgraph.builder() as _:
            _.add_node("root_value")
            _.add_predicate("has_child", "child_value")
            _.up()
            _.add_predicate("has_sibling", "sibling_value")

        with mgraph.data() as _:
            assert len(_.nodes()) == 3
            assert len(_.edges()) == 2

    def test_path_mode_index_works(self):                                                   # Verify index works with path-mode graphs
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            node1 = _.new_value("indexed_value")
            node2 = _.new_value("another_value")
            _.connect_nodes(node1, node2)

        with mgraph.index() as _:
            stats = _.stats()
            assert stats['index_data']['edge_to_nodes'] == 1

    def test__bug__path_mode_query_works(self):                                                   # Verify query works with path-mode graphs
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            node1 = _.new_value("query_test")
            node2 = _.new_value("connected")
            _.connect_nodes(node1, node2)

        #with mgraph.query() as _:
            #nodes = _.with_nodes().go()                # todo: add with_nodes (or equivalent)
            #assert len(nodes) == 2

    def test_path_mode_roundtrip(self):                                                     # Verify path-mode graphs survive serialization/deserialization
        # Create minimal graph
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            _.new_value("test value")

        json_data = mgraph.graph.model.data.json()

        # Reload
        restored = Schema__MGraph__Graph.from_json(json_data)

        # Should have one node with correct value
        assert len(restored.nodes) == 1
        node = list(restored.nodes.values())[0]
        assert node.node_data.value == "test value"

    def test_path_mode_export_works(self):                                                  # Verify export works with path-mode graphs
        mgraph = create_empty_mgraph()

        with mgraph.edit() as _:
            node1 = _.new_value("export_test")
            node2 = _.new_value("to_export")
            _.connect_nodes(node1, node2)

        json_export = mgraph.export().to__json()

        assert 'nodes' in json_export
        assert 'edges' in json_export