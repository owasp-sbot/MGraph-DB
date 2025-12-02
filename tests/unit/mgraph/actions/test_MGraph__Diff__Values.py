from unittest                                                       import TestCase
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.mgraph.actions.MGraph__Diff__Values                  import MGraph__Diff__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data
from osbot_utils.testing.__                                         import __


class test_MGraph__Diff__Values(TestCase):

    def setUp(self):
        self.graph_a = MGraph()                                                        # Create fresh graphs for each test
        self.graph_b = MGraph()
        self.differ  = MGraph__Diff__Values(graph1=self.graph_a, graph2=self.graph_b)

    def test_init(self):                                                              # Test initialization
        assert self.differ.graph1 == self.graph_a
        assert self.differ.graph2 == self.graph_b

    def test_get_values_by_type(self):                                               # Test getting values by type
        value_data = Schema__MGraph__Node__Value__Data(value="test", value_type=str)
        node_value = Schema__MGraph__Node__Value      (node_data=value_data)

        with self.graph_a.edit() as edit:                                             # Add value node to graph A
            edit.add_node(node_value).set_node_type(Schema__MGraph__Node__Value)

        values = self.differ.get_values_by_type(self.graph_a, str)
        assert len(values)              == 1
        assert list(values.values())[0] == "test"
        assert values                   == {'a987e948e2': 'test'}

    def test_compare_identical_graphs(self):                                          # Test comparing identical graphs
        diff = self.differ.compare([str])                                            # Compare with no values
        assert diff.obj() == __(added_values   = __(),
                                removed_values = __())

    def test_compare_different_values(self):                                        # Test comparing graphs with different values
        class TestEdge(Schema__MGraph__Edge): pass                                  # Define test edge type


        with self.graph_a.edit() as edit_a:                                         # Add different values to each graph
            value_data_a = Schema__MGraph__Node__Value__Data(value="value_a", value_type=str)
            node_a = edit_a.add_node(Schema__MGraph__Node__Value(node_data=value_data_a))

        assert node_a.node_data.obj() == __(value_type='builtins.str', value='value_a', key='')
        assert node_a.node_type       is Schema__MGraph__Node__Value

        with self.graph_b.edit() as edit_b:
            value_data_b = Schema__MGraph__Node__Value__Data(value="value_b", value_type=str)
            node_b = edit_b.add_node(Schema__MGraph__Node__Value(node_data=value_data_b))

        diff = self.differ.compare([str])
        assert diff.json() == { 'added_values'  : {'builtins.str': ['value_a']},
                                'removed_values': {'builtins.str': ['value_b']}}

        assert diff.added_values  [str] == {"value_a"}                              # Check values were properly categorized
        assert diff.removed_values[str] == {"value_b"}

    def test_multiple_value_types(self):                                           # Test comparing multiple value types
        # Add different types of values to each graph
        with self.graph_a.edit() as edit_a:
            str_data_a = Schema__MGraph__Node__Value__Data(value="str_a", value_type=str)
            int_data_a = Schema__MGraph__Node__Value__Data(value="42"   , value_type=int)
            edit_a.add_node(Schema__MGraph__Node__Value(node_data=str_data_a))
            edit_a.add_node(Schema__MGraph__Node__Value(node_data=int_data_a))

        with self.graph_b.edit() as edit_b:
            str_data_b = Schema__MGraph__Node__Value__Data(value="str_b", value_type=str)
            int_data_b = Schema__MGraph__Node__Value__Data(value="42"   , value_type=int)
            edit_b.add_node(Schema__MGraph__Node__Value(node_data=str_data_b))
            edit_b.add_node(Schema__MGraph__Node__Value(node_data=int_data_b))

        diff = self.differ.compare([str, int])
        assert diff.obj()  == __( added_values =__(builtins_str=['str_a']),
                                  removed_values=__(builtins_str=['str_b']))
        assert diff.json() == { 'added_values'  : { 'builtins.str': ['str_a']},
                                'removed_values': { 'builtins.str': ['str_b']}}

        assert str in diff.added_values
        assert str in diff.removed_values
        assert "str_a" in diff.added_values[str]
        assert "str_b" in diff.removed_values[str]
        assert int not in diff.added_values                                        # Integer value was the same
        assert int not in diff.removed_values

    def test_empty_graphs(self):                                                  # Test comparing empty graphs
        diff = self.differ.compare([str, int])                                    # Compare empty graphs

        assert diff.obj() == __(added_values   = __(),
                                removed_values = __())

    def test_value_with_key(self):                                              # Test values with keys
        with self.graph_a.edit() as edit_a:
            value_data = Schema__MGraph__Node__Value__Data(value      = "test"    ,
                                                           value_type = str       ,
                                                           key        = "test_key")
            node_value = Schema__MGraph__Node__Value(node_data=value_data)
            edit_a.add_node(node_value)

        values = self.differ.get_values_by_type(self.graph_a, str)
        assert values             == {'test_key': 'test'}
        assert "test_key"         in values                                     # Check that key is used as dictionary key
        assert values["test_key"] == "test"                                     # Check value is properly stored

    # todo see if need this changed_relationships diff capability
    # def test_compare_changed_relationships(self):                                   # Test comparing relationship changes
    #     class TestEdge(Schema__MGraph__Edge): pass
    #
    #     # Setup common value nodes
    #     value_data_common = Schema__MGraph__Node__Value__Data(value="common", value_type=str)
    #     node_common = Schema__MGraph__Node__Value(node_data=value_data_common)
    #
    #     # Setup target value nodes
    #     value_data_target_a = Schema__MGraph__Node__Value__Data(value="target_a", value_type=str)
    #     value_data_target_b = Schema__MGraph__Node__Value__Data(value="target_b", value_type=str)
    #
    #     with self.graph_a.edit() as edit_a:
    #         common_a = edit_a.add_node(node_common)
    #         target_a = edit_a.add_node(Schema__MGraph__Node__Value(node_data=value_data_target_a))
    #         edge_a = edit_a.new_edge(from_node_id=common_a.node_id,
    #                                to_node_id=target_a.node_id,
    #                                edge_type=TestEdge)
    #
    #     with self.graph_b.edit() as edit_b:
    #         common_b = edit_b.add_node(node_common)
    #         target_b = edit_b.add_node(Schema__MGraph__Node__Value(node_data=value_data_target_b))
    #         edge_b = edit_b.new_edge(from_node_id=common_b.node_id,
    #                                to_node_id=target_b.node_id,
    #                                edge_type=TestEdge)
    #
    #     diff = self.differ.compare([str])
    #
    #     assert "common" in diff.changed_relationships
    #     assert TestEdge in diff.changed_relationships["common"]
    #     assert diff.changed_relationships["common"][TestEdge] == {"target_a", "target_b"}

    # def test_complex_relationship_changes(self):                                # Test complex relationship changes
    #     class EdgeTypeA(Schema__MGraph__Edge): pass
    #     class EdgeTypeB(Schema__MGraph__Edge): pass
    #
    #     # Create value nodes
    #     value_data_source = Schema__MGraph__Node__Value__Data(value="source", value_type=str)
    #     value_data_target1 = Schema__MGraph__Node__Value__Data(value="target1", value_type=str)
    #     value_data_target2 = Schema__MGraph__Node__Value__Data(value="target2", value_type=str)
    #
    #     with self.graph_a.edit() as edit_a:
    #         source_a = edit_a.add_node(Schema__MGraph__Node__Value(node_data=value_data_source))
    #         target1_a = edit_a.add_node(Schema__MGraph__Node__Value(node_data=value_data_target1))
    #         # Graph A: source -> target1 with EdgeTypeA
    #         edit_a.new_edge(from_node_id=source_a.node_id,
    #                       to_node_id=target1_a.node_id,
    #                       edge_type=EdgeTypeA)
    #
    #     with self.graph_b.edit() as edit_b:
    #         source_b = edit_b.add_node(Schema__MGraph__Node__Value(node_data=value_data_source))
    #         target2_b = edit_b.add_node(Schema__MGraph__Node__Value(node_data=value_data_target2))
    #         # Graph B: source -> target2 with EdgeTypeB
    #         edit_b.new_edge(from_node_id=source_b.node_id,
    #                       to_node_id=target2_b.node_id,
    #                       edge_type=EdgeTypeB)
    #
    #     # Override get_edge_types_for_value to return our test edge types
    #     def get_edge_types(value_type: Type) -> list[Type[Schema__MGraph__Edge]]:
    #         return [EdgeTypeA, EdgeTypeB]
    #     self.differ.get_edge_types_for_value = get_edge_types
    #
    #     diff = self.differ.compare([str])
    #
    #     # Check that both relationship changes were captured
    #     assert "source" in diff.changed_relationships
    #     assert EdgeTypeA in diff.changed_relationships["source"]
    #     assert EdgeTypeB in diff.changed_relationships["source"]
    #     assert "target1" in diff.changed_relationships["source"][EdgeTypeA]
    #     assert "target2" in diff.changed_relationships["source"][EdgeTypeB]

    # def test_get_edge_types_for_value(self):                                     # Test getting edge types for value
    #     edge_types = self.differ.get_edge_types_for_value(str)
    #     assert edge_types == []                                                   # Default implementation returns empty list