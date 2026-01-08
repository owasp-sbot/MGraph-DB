"""
Performance tests for Model__MGraph__Node__Factory

These tests establish baseline performance metrics for node creation operations.
They can be run against both the original Model__MGraph__Graph.new_node() and
the refactored Model__MGraph__Node__Factory.create_node() to verify no regression.

Usage:
    pytest test_Model__MGraph__Node__Factory__performance.py -v

    # Run with detailed output
    pytest test_Model__MGraph__Node__Factory__performance.py -v -s
"""

from unittest                                                               import TestCase
from osbot_utils.helpers.performance.Performance_Measure__Session           import Perf
from mgraph_db.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node__Factory                   import Model__MGraph__Node__Factory
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                         import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                          import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                    import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                         import Schema__MGraph__Types


class Simple_Node      (Schema__MGraph__Node     ): pass                                    # Test node types
class Custom_Node      (Schema__MGraph__Node     ): pass
class Custom_Node_Data (Schema__MGraph__Node__Data):
    custom_value: str = ""

# todo: remove these prints with asserts once the performance improvements have been done
#     :
#     : for reference, for version v1.14.1, these are the stats
#
#     ============================== 79 passed in 1.02s ==============================
# create_100_nodes               | score: 5,900,000 ns  | raw: 5,933,094 ns
# create_10_nodes                | score: 600,000 ns    | raw: 559,024 ns
#
# --- Cold vs Warm Cache ---
# cold_cache_creation            | score:  80,000 ns    | raw:  75,088 ns
# warm_cache_creation            | score:  60,000 ns    | raw:  63,160 ns
#
# --- Factory vs Graph Direct Comparison ---
# via_factory                    | score:  60,000 ns    | raw:  57,138 ns
# via_graph                      | score:  60,000 ns    | raw:  64,785 ns
# create_node_complete           | score:  60,000 ns    | raw:  63,061 ns
# create_node_default            | score:  60,000 ns    | raw:  56,138 ns
# create_node_explicit           | score:  60,000 ns    | raw:  62,187 ns
# create_factory                 | score:  20,000 ns    | raw:  19,278 ns
#
# --- Type Resolution Steps ---
# resolve_types                  | score:     500 ns    | raw:     498 ns
# get_annotations                | score:     300 ns    | raw:     257 ns
# split_kwargs                   | score:     600 ns    | raw:     578 ns
# add_node                       | score:  50,000 ns    | raw:  50,891 ns
# create_and_delete              | score:  80,000 ns    | raw:  76,885 ns
# create_graph                   | score: 100,000 ns    | raw:  95,928 ns
# new_edge                       | score:  70,000 ns    | raw:  68,217 ns
# new_node                       | score:  60,000 ns    | raw:  62,856 ns
# retrieve_node                  | score:  20,000 ns    | raw:  21,656 ns
#
# --- Node Creation Scaling ---
# create_10                      | score: 600,000 ns    | raw: 641,201 ns
# create_50                      | score: 3,200,000 ns  | raw: 3,223,837 ns
# create_100                     | score: 6,300,000 ns  | raw: 6,289,552 ns
# create_10                      | score: 500,000 ns    | raw: 540,679 ns
# create_factory                 | score:  20,000 ns    | raw:  19,606 ns
# create_node                    | score:  60,000 ns    | raw:  64,076 ns

class test_Model__MGraph__Node__Factory__performance(TestCase):
    """Performance benchmarks for node creation operations.

    These tests establish baselines that can be used to:
    1. Compare original vs refactored implementation
    2. Detect performance regressions
    3. Guide future optimizations
    """

    @classmethod
    def setUpClass(cls):                                                                    # Setup shared test fixtures and perf session
        cls.session      = Perf(assert_enabled=False)                                       # Disable assertions for baseline
        cls.schema_types = Schema__MGraph__Types(node_type = Simple_Node          ,
                                                 edge_type = Schema__MGraph__Edge )

        # Time thresholds (in nanoseconds) - adjust based on actual measurements
        cls.time_50_kns   =    50_000                                                       # 50µs
        cls.time_100_kns  =   100_000                                                       # 100µs
        cls.time_200_kns  =   200_000                                                       # 200µs
        cls.time_500_kns  =   500_000                                                       # 500µs
        cls.time_1_ms     = 1_000_000                                                       # 1ms

    def _create_fresh_graph(self):                                                          # Helper to create fresh graph
        graph_data = Schema__MGraph__Graph(schema_types = self.schema_types    ,
                                           graph_type   = Schema__MGraph__Graph)
        return Model__MGraph__Graph(data=graph_data)

    def _create_factory(self, graph):                                                       # Helper to create factory
        return Model__MGraph__Node__Factory(graph=graph)

    # --- Factory Construction Performance ---

    def test__perf__factory_construction(self):                                             # Measure factory instantiation cost
        graph = self._create_fresh_graph()

        def create_factory():
            return Model__MGraph__Node__Factory(graph=graph)

        with self.session as _:
            _.measure__fast(create_factory).print()
            # Factory construction should be very fast (<100µs)

    # --- Single Node Creation Performance ---

    def test__perf__create_node__default_type(self):                                        # Measure node creation with default type
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def create_node_default():
            return factory.create_node()

        with self.session as _:
            _.measure__fast(create_node_default).print()

    def test__perf__create_node__explicit_type(self):                                       # Measure node creation with explicit node_type
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def create_node_explicit():
            return factory.create_node(node_type=Custom_Node)

        with self.session as _:
            _.measure__fast(create_node_explicit).print()

    def test__perf__create_node__complete_spec(self):                                       # Measure fast path with complete spec
        graph     = self._create_fresh_graph()
        factory   = self._create_factory(graph)
        node_data = Custom_Node_Data(custom_value="test")

        def create_node_complete():
            return factory.create_node(node_type=Custom_Node, node_data=node_data)

        with self.session as _:
            _.measure__fast(create_node_complete).print()
            # Fast path should be quicker than type resolution path

    # --- Comparison: Factory vs Direct Graph Method ---

    def test__perf__comparison__factory_vs_graph(self):                                     # Compare factory.create_node() vs graph.new_node()
        graph_factory = self._create_fresh_graph()
        graph_direct  = self._create_fresh_graph()
        factory       = self._create_factory(graph_factory)

        def via_factory():
            return factory.create_node()

        def via_graph():
            return graph_direct.new_node()

        with self.session as _:
            print("\n--- Factory vs Graph Direct Comparison ---")
            _.measure__fast(via_factory).print()
            _.measure__fast(via_graph  ).print()
            # Both should be comparable - factory is a refactor, not optimization

    # --- Batch Creation Performance ---

    def test__perf__batch_creation__10_nodes(self):                                         # Measure creating 10 nodes
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def create_10_nodes():
            for _ in range(10):
                factory.create_node()

        with self.session as _:
            _.measure__fast(create_10_nodes).print()

    def test__perf__batch_creation__100_nodes(self):                                        # Measure creating 100 nodes
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def create_100_nodes():
            for _ in range(100):
                factory.create_node()

        with self.session as _:
            _.measure__quick(create_100_nodes).print()                                      # Use quick mode - slower operation

    # --- Cache Effectiveness ---

    def test__perf__cache__cold_vs_warm(self):                                              # Compare cold cache vs warm cache performance
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def cold_cache_creation():
            factory.clear_caches()
            return factory.create_node(node_type=Custom_Node)

        # Warm up the cache first
        factory.create_node(node_type=Custom_Node)

        def warm_cache_creation():
            return factory.create_node(node_type=Custom_Node)

        with self.session as _:
            print("\n--- Cold vs Warm Cache ---")
            _.measure__fast(cold_cache_creation).print()
            _.measure__fast(warm_cache_creation).print()
            # Warm cache should be faster due to annotation caching

    # --- Type Resolution Overhead ---

    def test__perf__type_resolution__steps(self):                                           # Measure individual type resolution steps
        graph   = self._create_fresh_graph()
        factory = self._create_factory(graph)

        def resolve_types():
            return factory._resolve_node_types({'node_type': Custom_Node})

        def get_annotations():
            return factory._get_type_annotations(Custom_Node)

        def split_kwargs():
            return factory._split_kwargs({}, Custom_Node, Schema__MGraph__Node__Data)

        with self.session as _:
            print("\n--- Type Resolution Steps ---")
            _.measure__fast(resolve_types   ).print()
            _.measure__fast(get_annotations ).print()
            _.measure__fast(split_kwargs    ).print()


class test_Model__MGraph__Graph__Performance(TestCase):
    """Performance benchmarks for Model__MGraph__Graph operations.

    Establishes baselines for graph operations that can be compared
    before and after optimizations.
    """

    @classmethod
    def setUpClass(cls):
        cls.session      = Perf(assert_enabled=False)
        cls.schema_types = Schema__MGraph__Types(node_type = Simple_Node          ,
                                                 edge_type = Schema__MGraph__Edge )

    def _create_fresh_graph(self):
        graph_data = Schema__MGraph__Graph(schema_types = self.schema_types    ,
                                           graph_type   = Schema__MGraph__Graph)
        return Model__MGraph__Graph(data=graph_data)

    # --- Graph Construction ---

    def test__perf__graph_construction(self):                                               # Measure graph instantiation
        def create_graph():
            graph_data = Schema__MGraph__Graph(schema_types = self.schema_types    ,
                                               graph_type   = Schema__MGraph__Graph)
            return Model__MGraph__Graph(data=graph_data)

        with self.session as _:
            _.measure__fast(create_graph).print()

    # --- Node Operations ---

    def test__perf__new_node(self):                                                         # Measure graph.new_node()
        graph = self._create_fresh_graph()

        def new_node():
            return graph.new_node()

        with self.session as _:
            _.measure__fast(new_node).print()

    def test__perf__add_node(self):                                                         # Measure graph.add_node() with pre-created node
        graph = self._create_fresh_graph()

        def add_node():
            node = Simple_Node()
            return graph.add_node(node)

        with self.session as _:
            _.measure__fast(add_node).print()

    def test__perf__node_retrieval(self):                                                   # Measure node lookup by ID
        graph   = self._create_fresh_graph()
        node    = graph.new_node()
        node_id = node.node_id

        def retrieve_node():
            return graph.node(node_id)

        with self.session as _:
            _.measure__fast(retrieve_node).print()

    def test__perf__delete_node(self):                                                      # Measure node deletion
        graph = self._create_fresh_graph()

        def create_and_delete():
            node    = graph.new_node()
            node_id = node.node_id
            return graph.delete_node(node_id)

        with self.session as _:
            _.measure__fast(create_and_delete).print()

    # --- Edge Operations ---

    def test__perf__new_edge(self):                                                         # Measure edge creation
        graph   = self._create_fresh_graph()
        node_1  = graph.new_node()
        node_2  = graph.new_node()

        def new_edge():
            return graph.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        with self.session as _:
            _.measure__fast(new_edge).print()

    # --- Scaling Tests ---

    def test__perf__scaling__nodes_10_50_100(self):                                         # Measure scaling behavior
        graph = self._create_fresh_graph()

        def create_10():
            for _ in range(10):
                graph.new_node()

        def create_50():
            for _ in range(50):
                graph.new_node()

        def create_100():
            for _ in range(100):
                graph.new_node()

        with self.session as _:
            print("\n--- Node Creation Scaling ---")
            _.measure__fast (create_10 ).print()
            _.measure__fast (create_50 ).print()
            _.measure__quick(create_100).print()


class test_Performance__Regression_Suite(TestCase):
    """Regression tests with assertions to catch performance degradation.

    These tests will fail if performance degrades beyond acceptable thresholds.
    Run before and after changes to verify no regression.
    """

    @classmethod
    def setUpClass(cls):
        cls.session      = Perf(assert_enabled=True)                                        # Enable assertions
        cls.schema_types = Schema__MGraph__Types(node_type = Simple_Node          ,
                                                 edge_type = Schema__MGraph__Edge )

        # Baseline thresholds - adjust based on measured performance
        # These are conservative to account for CI variability
        cls.factory_construction_max = 100_000                                              # 100µs
        cls.single_node_creation_max = 500_000                                              # 500µs
        cls.batch_10_nodes_max       = 5_000_000                                            # 5ms

    def _create_fresh_graph(self):
        graph_data = Schema__MGraph__Graph(schema_types = self.schema_types    ,
                                           graph_type   = Schema__MGraph__Graph)
        return Model__MGraph__Graph(data=graph_data)

    def test__regression__factory_construction(self):                                       # Factory construction should stay fast
        graph = self._create_fresh_graph()

        def create_factory():
            return Model__MGraph__Node__Factory(graph=graph)

        with self.session as _:
            _.measure__fast(create_factory).print().assert_time__less_than(
                self.factory_construction_max
            )

    def test__regression__single_node_creation(self):                                       # Single node creation should stay bounded
        graph   = self._create_fresh_graph()
        factory = Model__MGraph__Node__Factory(graph=graph)

        def create_node():
            return factory.create_node()

        with self.session as _:
            _.measure__fast(create_node).print().assert_time__less_than(
                self.single_node_creation_max
            )

    def test__regression__batch_10_nodes(self):                                             # Batch creation should scale linearly
        graph   = self._create_fresh_graph()
        factory = Model__MGraph__Node__Factory(graph=graph)

        def create_10():
            for _ in range(10):
                factory.create_node()

        with self.session as _:
            _.measure__fast(create_10).print().assert_time__less_than(
                self.batch_10_nodes_max
            )