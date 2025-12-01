from unittest                                                   import TestCase
from mgraph_db.mgraph.schemas.identifiers.Edge_Path             import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Graph_Path            import Graph_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path             import Node_Path
from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path    import Safe_Str__Graph__Path


class test_Path__type_safety(TestCase):

    def test_type_safety_distinct_classes(self):
        """Test that path types are distinct classes."""
        node_path  = Node_Path ("html.body")
        edge_path  = Edge_Path ("contains" )
        graph_path = Graph_Path("my.graph" )

        assert isinstance(node_path , Node_Path )
        assert isinstance(edge_path , Edge_Path )
        assert isinstance(graph_path, Graph_Path)

        assert isinstance(node_path , Safe_Str__Graph__Path)
        assert isinstance(edge_path , Safe_Str__Graph__Path)
        assert isinstance(graph_path, Safe_Str__Graph__Path)

    def test_type_safety_not_interchangeable(self):
        """Test that different path types are not equal even with same value."""
        node_path  = Node_Path ("same.path")
        edge_path  = Edge_Path ("same.path")
        graph_path = Graph_Path("same.path")

        # They should NOT be equal because they are different types
        assert node_path != edge_path
        assert node_path != graph_path
        assert edge_path != graph_path

    def test_same_type_same_value_equal(self):
        """Test that same type with same value are equal."""
        node_path_1 = Node_Path("html.body")
        node_path_2 = Node_Path("html.body")

        assert node_path_1 == node_path_2

    def test_same_type_different_value_not_equal(self):
        """Test that same type with different values are not equal."""
        node_path_1 = Node_Path("html.body")
        node_path_2 = Node_Path("html.head")

        assert node_path_1 != node_path_2

    def test_hashable_for_dict_keys(self):
        """Test that path types can be used as dictionary keys."""
        node_path_1 = Node_Path("path.one")
        node_path_2 = Node_Path("path.two")
        edge_path_1 = Edge_Path("edge.one")

        # Should be usable as dict keys
        test_dict = {
            node_path_1: "value1",
            node_path_2: "value2",
            edge_path_1: "value3",
        }

        assert test_dict[node_path_1] == "value1"
        assert test_dict[node_path_2] == "value2"
        assert test_dict[edge_path_1] == "value3"

    def test_hashable_for_set_membership(self):
        """Test that path types can be used in sets."""
        node_path_1 = Node_Path("path.one")
        node_path_2 = Node_Path("path.one")  # Same value
        node_path_3 = Node_Path("path.two")  # Different value

        test_set = {node_path_1, node_path_2, node_path_3}

        # node_path_1 and node_path_2 should be the same in the set
        assert len(test_set) == 2
        assert node_path_1 in test_set
        assert node_path_3 in test_set