from unittest                                                               import TestCase
from mgraph_db.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node                            import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Node__Factory                   import Model__MGraph__Node__Factory
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                         import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                    import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                         import Schema__MGraph__Types
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict       import Type_Safe__Dict
from osbot_utils.utils.Objects                                              import base_classes


class Simple_Node     (Schema__MGraph__Node     ): pass                                     # Helper classes for testing
class Custom_Node     (Schema__MGraph__Node     ): pass
class Another_Node    (Schema__MGraph__Node     ): pass
class Custom_Node_Data(Schema__MGraph__Node__Data):
    custom_value: str = ""



class test_Model__MGraph__Node__Factory(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Setup shared test fixtures
        cls.schema_types = Schema__MGraph__Types(node_type = Simple_Node          ,
                                                 edge_type = Schema__MGraph__Edge )

    def setUp(self):                                                                        # Fresh graph and factory for each test
        self.graph_data = Schema__MGraph__Graph(schema_types = self.schema_types    ,
                                                graph_type   = Schema__MGraph__Graph)
        self.graph      = Model__MGraph__Graph (data         = self.graph_data      )
        self.factory    = Model__MGraph__Node__Factory(graph = self.graph           )

    def test__init__(self):                                                                 # Test factory initialization
        with self.factory as _:
            assert type(_)                         is Model__MGraph__Node__Factory
            assert base_classes(_)                 == [Type_Safe, object]
            assert _.graph                         is self.graph
            assert type(_._type_annotations_cache) is Type_Safe__Dict
            assert type(_._data_type_cache       ) is Type_Safe__Dict
            assert len(_._type_annotations_cache)  == 0                                     # Caches start empty
            assert len(_._data_type_cache       )  == 0

    def test_create_node__default_type(self):                                               # Test node creation with default type from schema_types
        with self.factory as _:
            node = _.create_node()

            assert type(node)       is Model__MGraph__Node
            assert node.node_type   is Simple_Node                                          # Uses schema_types.node_type
            assert node.node_id     in self.graph.data.nodes                                # Node added to graph

    def test_create_node__with_node_type(self):                                             # Test node creation with explicit node_type
        with self.factory as _:
            node = _.create_node(node_type=Custom_Node)

            assert type(node)       is Model__MGraph__Node
            assert node.node_type   is Custom_Node
            assert node.node_id     in self.graph.data.nodes

    def test_create_node__with_complete_spec(self):                                         # Test fast path with node_type and node_data
        node_data = Custom_Node_Data(custom_value="test_value")

        with self.factory as _:
            node = _.create_node(node_type=Custom_Node, node_data=node_data)

            assert type(node)            is Model__MGraph__Node
            assert node.node_type        is Custom_Node
            assert node.data.node_data   is node_data

    def test_create_node__multiple_nodes(self):                                             # Test creating multiple nodes
        with self.factory as _:
            node_1 = _.create_node()
            node_2 = _.create_node(node_type=Custom_Node)
            node_3 = _.create_node(node_type=Another_Node)

            assert len(self.graph.data.nodes) == 3
            assert node_1.node_id != node_2.node_id
            assert node_2.node_id != node_3.node_id
            assert node_1.node_type is Simple_Node
            assert node_2.node_type is Custom_Node
            assert node_3.node_type is Another_Node

    # --- Type Resolution Tests ---

    def test__resolve_node_types__from_kwargs(self):                                        # Test type resolution when node_type in kwargs
        with self.factory as _:
            kwargs = {'node_type': Custom_Node}
            node_type, node_data_type, add_type = _._resolve_node_types(kwargs)

            assert node_type      is Custom_Node
            assert add_type       is False                                                  # Don't set when explicitly provided

    def test__resolve_node_types__from_schema_types(self):                                  # Test type resolution from graph's schema_types
        with self.factory as _:
            kwargs = {}
            node_type, node_data_type, add_type = _._resolve_node_types(kwargs)

            assert node_type is Simple_Node                                                 # From schema_types
            assert add_type  is True                                                        # Must set node_type

    def test__resolve_node_types__fallback(self):                                           # Test fallback to resolver defaults
        graph_data_no_schema = Schema__MGraph__Graph()                                      # No schema_types
        graph_no_schema      = Model__MGraph__Graph(data=graph_data_no_schema)
        factory              = Model__MGraph__Node__Factory(graph=graph_no_schema)

        with factory as _:
            kwargs = {}
            node_type, node_data_type, add_type = _._resolve_node_types(kwargs)

            assert node_type      is Schema__MGraph__Node                                   # Default from resolver
            assert add_type       is False

    # --- Kwargs Splitting Tests ---

    def test__split_kwargs(self):                                                           # Test kwargs splitting between node and data
        with self.factory as _:
            # node_id belongs to Schema__MGraph__Node, custom_value to Custom_Node_Data
            kwargs = {'node_id': 'test_id', 'some_other': 'value'}

            node_kwargs, data_kwargs = _._split_kwargs(kwargs, Simple_Node, Schema__MGraph__Node__Data)

            assert 'node_id' in node_kwargs                                                 # node_id goes to node
            assert 'some_other' not in node_kwargs                                          # Unknown kwargs ignored
            assert 'some_other' not in data_kwargs

    # --- Fast Path Tests ---

    def test__has_complete_node_spec__true(self):                                           # Test detection of complete spec
        with self.factory as _:
            kwargs = {'node_type': Custom_Node, 'node_data': Custom_Node_Data()}
            assert _._has_complete_node_spec(kwargs) is True

    def test__has_complete_node_spec__false_missing_data(self):                             # Test incomplete spec - missing node_data
        with self.factory as _:
            kwargs = {'node_type': Custom_Node}
            assert _._has_complete_node_spec(kwargs) is False

    def test__has_complete_node_spec__false_missing_type(self):                             # Test incomplete spec - missing node_type
        with self.factory as _:
            kwargs = {'node_data': Custom_Node_Data()}
            assert _._has_complete_node_spec(kwargs) is False

    def test__has_complete_node_spec__false_empty(self):                                    # Test empty kwargs
        with self.factory as _:
            assert _._has_complete_node_spec({}) is False

    # --- Cache Tests ---

    def test__get_type_annotations__caching(self):                                          # Test that annotations are cached
        with self.factory as _:
            assert len(_._type_annotations_cache) == 0

            annotations_1 = _._get_type_annotations(Simple_Node)
            assert len(_._type_annotations_cache) == 1

            annotations_2 = _._get_type_annotations(Simple_Node)                            # Should hit cache
            assert annotations_1 is annotations_2                                           # Same dict object
            assert len(_._type_annotations_cache) == 1                                      # No new entry

            _._get_type_annotations(Custom_Node)                                            # Different type
            assert len(_._type_annotations_cache) == 2

    def test_cache_stats(self):                                                             # Test cache statistics
        with self.factory as _:
            stats = _.cache_stats()
            assert stats == {'type_annotations_cached': 0, 'data_types_cached': 0}

            _.create_node()                                                                 # Triggers caching

            stats = _.cache_stats()
            assert stats['type_annotations_cached'] > 0

    def test_clear_caches(self):                                                            # Test cache clearing
        with self.factory as _:
            _.create_node()                                                                 # Populate caches
            assert len(_._type_annotations_cache) > 0

            result = _.clear_caches()

            assert result is _                                                              # Returns self for chaining
            assert len(_._type_annotations_cache) == 0
            assert len(_._data_type_cache      ) == 0

    # --- Node Data Creation Tests ---

    def test__create_node_data__none_for_base_schema(self):                                 # Test that base schema returns None
        with self.factory as _:
            result = _._create_node_data(Schema__MGraph__Node__Data, {})
            assert result is None

    def test__create_node_data__with_kwargs(self):                                          # Test node_data creation with kwargs
        with self.factory as _:
            result = _._create_node_data(Custom_Node_Data, {'custom_value': 'test'})

            assert type(result)        is Custom_Node_Data
            assert result.custom_value == 'test'

    # --- Integration Tests ---

    def test__integration__factory_matches_graph_new_node(self):                            # Verify factory produces same results as direct graph.new_node
        # Create nodes via factory
        factory_node_1 = self.factory.create_node()
        factory_node_2 = self.factory.create_node(node_type=Custom_Node)

        # Create fresh graph for comparison
        graph_data_2 = Schema__MGraph__Graph(schema_types=self.schema_types,
                                             graph_type  =Schema__MGraph__Graph)
        graph_2      = Model__MGraph__Graph(data=graph_data_2)

        # Create nodes via graph directly (original method)
        direct_node_1 = graph_2.new_node()
        direct_node_2 = graph_2.new_node(node_type=Custom_Node)

        # Compare structure (not IDs which are auto-generated)
        assert type(factory_node_1) == type(direct_node_1)
        assert type(factory_node_2) == type(direct_node_2)
        assert factory_node_1.node_type == direct_node_1.node_type
        assert factory_node_2.node_type == direct_node_2.node_type

    def test__integration__repeated_node_creation(self):                                    # Test many nodes created efficiently
        with self.factory as _:
            nodes = [_.create_node() for i in range(100)]

            assert len(nodes)                 == 100
            assert len(self.graph.data.nodes) == 100

            # All nodes should have unique IDs
            node_ids = [n.node_id for n in nodes]
            assert len(set(node_ids)) == 100


    def test__create_node__preserves_graph_integrity(self):                                 # Verify graph state after node creation
        initial_nodes = len(self.graph.data.nodes)

        with self.factory as _:
            _.create_node()
            _.create_node()
            _.create_node()

        assert len(self.graph.data.nodes) == initial_nodes + 3

    def test__factory_reuse_across_graphs(self):                                            # Test that factory is graph-specific
        graph_2      = Model__MGraph__Graph(data=Schema__MGraph__Graph(schema_types=self.schema_types))
        factory_2    = Model__MGraph__Node__Factory(graph=graph_2)

        node_1 = self.factory.create_node()
        node_2 = factory_2.create_node()

        assert node_1.node_id in self.graph.data.nodes
        assert node_1.node_id not in graph_2.data.nodes
        assert node_2.node_id in graph_2.data.nodes
        assert node_2.node_id not in self.graph.data.nodes