from unittest                                                   import TestCase
from mgraph_db.mgraph.schemas.identifiers.Graph_Path            import Graph_Path
from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path    import Safe_Str__Graph__Path


class test_Graph_Path(TestCase):

    def test_graph_path_creation(self):
        """Test Graph_Path creation with valid paths."""
        path = Graph_Path("service.users.graph")
        assert str(path) == "service.users.graph"

    def test_graph_path_inheritance(self):
        """Test that Graph_Path inherits from Safe_Str__Graph__Path."""
        path = Graph_Path("test.path")
        assert isinstance(path, Safe_Str__Graph__Path)


