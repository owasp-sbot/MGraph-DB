from unittest                                                       import TestCase
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id  import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from mgraph_db.utils.testing.MGraph__Test__Ids                      import MGraph__Test__Ids
from mgraph_db.utils.testing.mgraph_test_ids                        import mgraph_test_ids, test_ids


class test_mgraph_test_ids(TestCase):

    def test__context_manager__resets_on_entry(self):                                           # Test context manager resets counters
        test_ids.counter_node = 999                                                            # Set to non-zero

        with mgraph_test_ids() as _:
            assert _.counter_node == 0                                                   # Reset on entry

    def test__context_manager__returns_test_ids_instance(self):                                 # Test context manager yields _test_ids
        with mgraph_test_ids() as _:
            assert _           is test_ids
            assert type(_)     is MGraph__Test__Ids

    def test__patches_obj_id__direct_call(self):                                                # Test Obj_Id() returns deterministic value
        with mgraph_test_ids() as _:
            obj_id_1 = Obj_Id()
            obj_id_2 = Obj_Id()
            obj_id_3 = Obj_Id()

            assert str(obj_id_1)      == 'f0000001'                                             # Sequential with 'o' prefix
            assert str(obj_id_2)      == 'f0000002'
            assert str(obj_id_3)      == 'f0000003'
            assert _.counter_obj      == 3

    def test__patches_obj_id__via_graph_id(self):                                               # Test Graph_Id(Obj_Id()) uses 'a' prefix
        with mgraph_test_ids() as _:
            graph_id_1 = Graph_Id(Obj_Id())
            graph_id_2 = Graph_Id(Obj_Id())

            assert str(graph_id_1) == 'a0000001'                                             # Sequential with 'a' prefix
            assert str(graph_id_2) == 'a0000002'
            assert _.counter_graph == 2
            assert _.counter_node  == 0                                                  # Other counters unchanged
            assert _.counter_edge  == 0

    def test__patches_obj_id__via_node_id(self):                                                # Test Node_Id(Obj_Id()) uses 'd' prefix
        with mgraph_test_ids() as test_ids:
            node_id_1 = Node_Id(Obj_Id())
            node_id_2 = Node_Id(Obj_Id())
            node_id_3 = Node_Id(Obj_Id())

            assert str(node_id_1)     == 'c0000001'                                             # Sequential with 'd' prefix
            assert str(node_id_2)     == 'c0000002'
            assert str(node_id_3)     == 'c0000003'
            assert test_ids.counter_node  == 3
            assert test_ids.counter_graph == 0                                                  # Other counters unchanged
            assert test_ids.counter_edge  == 0

    def test__patches_obj_id__via_edge_id(self):                                                # Test Edge_Id(Obj_Id()) uses 'e' prefix
        with mgraph_test_ids() as test_ids:
            edge_id_1 = Edge_Id(Obj_Id())
            edge_id_2 = Edge_Id(Obj_Id())

            assert str(edge_id_1)     == 'e0000001'                                             # Sequential with 'e' prefix
            assert str(edge_id_2)     == 'e0000002'
            assert test_ids.counter_edge  == 2
            assert test_ids.counter_graph == 0                                                  # Other counters unchanged
            assert test_ids.counter_node  == 0

    def test__patches_obj_id__mixed_calls(self):                                                # Test mixed ID generation maintains separate counters
        with mgraph_test_ids() as test_ids:
            node_1  = Node_Id(Obj_Id())                                                         # d0000001
            edge_1  = Edge_Id(Obj_Id())                                                         # e0000001
            graph_1 = Graph_Id(Obj_Id())                                                        # a0000001
            node_2  = Node_Id(Obj_Id())                                                         # d0000002
            edge_2  = Edge_Id(Obj_Id())                                                         # e0000002
            node_3  = Node_Id(Obj_Id())                                                         # d0000003

            assert str(node_1)        == 'c0000001'
            assert str(edge_1)        == 'e0000001'
            assert str(graph_1)       == 'a0000001'
            assert str(node_2)        == 'c0000002'
            assert str(edge_2)        == 'e0000002'
            assert str(node_3)        == 'c0000003'

            assert test_ids.obj()     == __(counter_graph = 1,
                                            counter_node  = 3,
                                            counter_edge  = 2,
                                            counter_obj   = 0)

    def test__context_manager__restores_after_exit(self):                                       # Test Obj_Id returns random values after context exits
        with mgraph_test_ids():
            deterministic_id = str(Obj_Id())
            assert deterministic_id   == 'f0000001'                                             # Deterministic inside context

        random_id = str(Obj_Id())
        assert random_id              != 'f0000002'                                             # Random outside context
        assert len(random_id)         == 8                                                      # Standard Obj_Id length

    def test__multiple_context_managers__reset_each_time(self):                                 # Test each context manager invocation resets counters
        with mgraph_test_ids() as test_ids_1:
            Node_Id(Obj_Id())
            Node_Id(Obj_Id())
            assert test_ids_1.counter_node == 2

        with mgraph_test_ids() as test_ids_2:
            node_id = Node_Id(Obj_Id())
            assert str(node_id)       == 'c0000001'                                             # Starts fresh
            assert test_ids_2.counter_node == 1

    def test__id_type_detection__is_case_sensitive(self):                                       # Test detection works with exact class names
        with mgraph_test_ids() as test_ids:
            node_id = Node_Id(Obj_Id())                                                         # Node_Id detected
            edge_id = Edge_Id(Obj_Id())                                                         # Edge_Id detected

            assert str(node_id)       == 'c0000001'
            assert str(edge_id)       == 'e0000001'

