from unittest                                                   import TestCase
from mgraph_db.mgraph.schemas.identifiers.Edge_Path             import Edge_Path
from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path    import Safe_Str__Graph__Path


class test_Edge_Path(TestCase):

    def test_edge_path_creation(self):
        """Test Edge_Path creation with valid paths."""
        path = Edge_Path("relationship.contains")
        assert str(path) == "relationship.contains"

    def test_edge_path_inheritance(self):
        """Test that Edge_Path inherits from Safe_Str__Graph__Path."""
        path = Edge_Path("test.path")
        assert isinstance(path, Safe_Str__Graph__Path)