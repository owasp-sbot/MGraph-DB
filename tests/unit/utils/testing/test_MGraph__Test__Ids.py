from unittest                                  import TestCase
from osbot_utils.testing.__                    import __
from osbot_utils.utils.Objects                 import base_classes
from osbot_utils.type_safe.Type_Safe           import Type_Safe
from mgraph_db.utils.testing.MGraph__Test__Ids import MGraph__Test__Ids


class test_MGraph__Test__Ids(TestCase):

    def test__init__(self):                                                                     # Test MGraph__Test__Ids initialization
        with MGraph__Test__Ids() as _:
            assert type(_)            is MGraph__Test__Ids
            assert base_classes(_)    == [Type_Safe, object]
            assert _.counter_graph    == 0
            assert _.counter_node     == 0
            assert _.counter_edge     == 0
            assert _.counter_obj      == 0
            assert _.obj()            == __(counter_graph = 0,
                                            counter_node  = 0,
                                            counter_edge  = 0,
                                            counter_obj   = 0)

    def test_reset(self):                                                                       # Test reset method clears all counters
        with MGraph__Test__Ids() as _:
            _.counter_graph = 5                                                                 # Set counters to non-zero values
            _.counter_node  = 10
            _.counter_edge  = 15
            _.counter_obj   = 20

            result = _.reset()                                                                  # Reset and verify

            assert result             is _                                                      # Returns self for chaining
            assert _.counter_graph    == 0
            assert _.counter_node     == 0
            assert _.counter_edge     == 0
            assert _.counter_obj      == 0

    def test_next_graph_id(self):                                                               # Test Graph_Id generation with 'a' prefix
        with MGraph__Test__Ids() as _:
            assert _.next_graph_id()  == 'a0000001'                                             # First call
            assert _.next_graph_id()  == 'a0000002'                                             # Sequential
            assert _.next_graph_id()  == 'a0000003'
            assert _.counter_graph    == 3                                                      # Counter tracks calls

    def test_next_node_id(self):                                                                # Test Node_Id generation with 'd' prefix
        with MGraph__Test__Ids() as _:
            assert _.next_node_id()   == 'c0000001'                                             # First call
            assert _.next_node_id()   == 'c0000002'                                             # Sequential
            assert _.next_node_id()   == 'c0000003'
            assert _.counter_node     == 3                                                      # Counter tracks calls

    def test_next_edge_id(self):                                                                # Test Edge_Id generation with 'e' prefix
        with MGraph__Test__Ids() as _:
            assert _.next_edge_id()   == 'e0000001'                                             # First call
            assert _.next_edge_id()   == 'e0000002'                                             # Sequential
            assert _.next_edge_id()   == 'e0000003'
            assert _.counter_edge     == 3                                                      # Counter tracks calls

    def test_next_obj_id(self):                                                                 # Test direct Obj_Id generation with 'o' prefix
        with MGraph__Test__Ids() as _:
            assert _.next_obj_id()    == 'f0000001'                                             # First call
            assert _.next_obj_id()    == 'f0000002'                                             # Sequential
            assert _.next_obj_id()    == 'f0000003'
            assert _.counter_obj      == 3                                                      # Counter tracks calls

    def test_next_id_from_context__direct_obj_id(self):                                         # Test context detection falls back to obj_id
        with MGraph__Test__Ids() as _:
            result = _.next_id_from_context()                                                   # Called directly, not wrapped
            assert result             == 'f0000001'                                             # Falls back to obj_id
            assert _.counter_obj      == 1

    def test__counters_are_independent(self):                                                   # Test each counter increments independently
        with MGraph__Test__Ids() as _:
            _.next_graph_id()                                                                   # Increment each type
            _.next_graph_id()
            _.next_node_id()
            _.next_edge_id()
            _.next_edge_id()
            _.next_edge_id()

            assert _.obj()            == __(counter_graph = 2,                                  # Each counter independent
                                            counter_node  = 1,
                                            counter_edge  = 3,
                                            counter_obj   = 0)

    def test__id_format_padding(self):                                                          # Test ID format uses 7-digit zero padding
        with MGraph__Test__Ids() as _:
            for i in range(999):                                                                # Generate many IDs
                _.next_node_id()

            assert _.next_node_id()   == 'c0001000'                                             # Properly padded
            assert len('d0001000')    == 8                                                      # Prefix + 7 digits



# class test_MGraph__Test__Ids__Integration(TestCase):
#
#     def test__with_mgraph_schema_creation(self):                                                # Test integration with actual MGraph schema classes
#         from mgraph_db.mgraph.schemas.Schema__MGraph__Graph import Schema__MGraph__Graph
#         from mgraph_db.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
#         from mgraph_db.mgraph.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
#
#         with mgraph_test_ids() as test_ids:
#             graph = Schema__MGraph__Graph()                                                     # Creates Graph_Id(Obj_Id())
#             node1 = Schema__MGraph__Node()                                                      # Creates Node_Id(Obj_Id())
#             node2 = Schema__MGraph__Node()
#             edge  = Schema__MGraph__Edge(from_node_id = node1.node_id,                          # Creates Edge_Id(Obj_Id())
#                                          to_node_id   = node2.node_id)
#
#             assert str(graph.graph_id) == 'a0000001'
#             assert str(node1.node_id)  == 'd0000001'
#             assert str(node2.node_id)  == 'd0000002'
#             assert str(edge.edge_id)   == 'e0000001'
#
#             assert test_ids.obj()      == __(counter_graph = 1,
#                                              counter_node  = 2,
#                                              counter_edge  = 1,
#                                              counter_obj   = 0)
#
#     def test__enables_deterministic_obj_comparison(self):                                       # Test enables .obj() comparisons in tests
#         from mgraph_db.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node
#
#         with mgraph_test_ids():
#             node = Schema__MGraph__Node()
#
#             assert node.obj()          == __(node_data = None           ,
#                                              node_path = None           ,
#                                              node_type = None           ,
#                                              node_id   = 'd0000001'     )
#
#     def test__repeated_test_runs_produce_same_ids(self):                                        # Test same code produces same IDs across runs
#         from mgraph_db.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node
#
#         def create_two_nodes():
#             node1 = Schema__MGraph__Node()
#             node2 = Schema__MGraph__Node()
#             return str(node1.node_id), str(node2.node_id)
#
#         with mgraph_test_ids():                                                                 # First run
#             ids_run_1 = create_two_nodes()
#
#         with mgraph_test_ids():                                                                 # Second run
#             ids_run_2 = create_two_nodes()
#
#         assert ids_run_1              == ids_run_2                                              # Same IDs both runs
#         assert ids_run_1              == ('d0000001', 'd0000002')