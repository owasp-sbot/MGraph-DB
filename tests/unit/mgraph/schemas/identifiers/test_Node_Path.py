from unittest                                                   import TestCase
from mgraph_db.mgraph.schemas.identifiers.Node_Path             import Node_Path
from mgraph_db.mgraph.schemas.safe_str.Safe_Str__Graph__Path    import Safe_Str__Graph__Path

class test_Node_Path(TestCase):

    def test_node_path_creation(self):
        """Test Node_Path creation with valid paths."""
        path = Node_Path("html.body.div.p[1]")
        assert str(path) == "html.body.div.p[1]"

    def test_node_path_inheritance(self):
        """Test that Node_Path inherits from Safe_Str__Graph__Path."""
        path = Node_Path("test.path")
        assert isinstance(path, Safe_Str__Graph__Path)


