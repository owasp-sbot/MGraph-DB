from unittest                                                       import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Paths                    import MGraph__Index__Paths
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data     import Schema__MGraph__Index__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class test_MGraph__Index__Paths(TestCase):

    def setUp(self):
        self.index_data  = Schema__MGraph__Index__Data()
        self.paths_index = MGraph__Index__Paths(index_data=self.index_data)

    def test__init__(self):                                                     # Test initialization
        with self.paths_index as _:
            assert type(_)            is MGraph__Index__Paths
            assert type(_.index_data) is Schema__MGraph__Index__Data
            assert _.nodes_by_path()  == {}
            assert _.edges_by_path()  == {}

    # =========================================================================
    # Node Path Add/Remove Tests
    # =========================================================================

    def test_index_node_path__with_path(self):                                  # Test indexing node with path
        node = Schema__MGraph__Node(node_path=Node_Path("test.path"))

        with self.paths_index as _:
            _.index_node_path(node)

            assert Node_Path("test.path") in _.nodes_by_path()
            assert node.node_id           in _.nodes_by_path()[Node_Path("test.path")]

    def test_index_node_path__without_path(self):                               # Test indexing node without path
        node = Schema__MGraph__Node()

        with self.paths_index as _:
            _.index_node_path(node)

            assert _.nodes_by_path() == {}                                      # No path added

    def test_index_node_path__multiple_nodes_same_path(self):                   # Test multiple nodes with same path
        path  = Node_Path("shared.path")
        node1 = Schema__MGraph__Node(node_path=path)
        node2 = Schema__MGraph__Node(node_path=path)

        with self.paths_index as _:
            _.index_node_path(node1)
            _.index_node_path(node2)

            assert len(_.nodes_by_path()[path]) == 2
            assert node1.node_id in _.nodes_by_path()[path]
            assert node2.node_id in _.nodes_by_path()[path]

    def test_remove_node_path__with_path(self):                                 # Test removing node path
        node = Schema__MGraph__Node(node_path=Node_Path("to.remove"))

        with self.paths_index as _:
            _.index_node_path(node)
            assert Node_Path("to.remove") in _.nodes_by_path()

            _.remove_node_path(node)
            assert Node_Path("to.remove") not in _.nodes_by_path()              # Empty set cleaned up

    def test_remove_node_path__without_path(self):                              # Test removing node without path
        node = Schema__MGraph__Node()

        with self.paths_index as _:
            _.remove_node_path(node)                                            # Should not crash

            assert _.nodes_by_path() == {}

    def test_remove_node_path__keeps_other_nodes(self):                         # Test removing one node keeps others
        path  = Node_Path("shared")
        node1 = Schema__MGraph__Node(node_path=path)
        node2 = Schema__MGraph__Node(node_path=path)

        with self.paths_index as _:
            _.index_node_path(node1)
            _.index_node_path(node2)

            _.remove_node_path(node1)

            assert path          in _.nodes_by_path()
            assert node1.node_id not in _.nodes_by_path()[path]
            assert node2.node_id     in _.nodes_by_path()[path]

    # =========================================================================
    # Edge Path Add/Remove Tests
    # =========================================================================

    def test_index_edge_path__with_path(self):                                  # Test indexing edge with path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id = node1.node_id          ,
                                     to_node_id   = node2.node_id          ,
                                     edge_path    = Edge_Path("edge.path") )

        with self.paths_index as _:
            _.index_edge_path(edge)

            assert Edge_Path("edge.path") in _.edges_by_path()
            assert edge.edge_id           in _.edges_by_path()[Edge_Path("edge.path")]

    def test_index_edge_path__without_path(self):                               # Test indexing edge without path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        with self.paths_index as _:
            _.index_edge_path(edge)

            assert _.edges_by_path() == {}

    def test_remove_edge_path__with_path(self):                                 # Test removing edge path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id = node1.node_id           ,
                                     to_node_id   = node2.node_id           ,
                                     edge_path    = Edge_Path("to.remove")  )

        with self.paths_index as _:
            _.index_edge_path(edge)
            assert Edge_Path("to.remove") in _.edges_by_path()

            _.remove_edge_path(edge)
            assert Edge_Path("to.remove") not in _.edges_by_path()

    def test_remove_edge_path__without_path(self):                              # Test removing edge without path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        with self.paths_index as _:
            _.remove_edge_path(edge)                                            # Should not crash

            assert _.edges_by_path() == {}

    def test_remove_edge_path_by_id__found(self):                               # Test removing edge path by ID
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id = node1.node_id           ,
                                     to_node_id   = node2.node_id           ,
                                     edge_path    = Edge_Path("by.id")      )

        with self.paths_index as _:
            _.index_edge_path(edge)

            _.remove_edge_path_by_id(edge.edge_id)

            assert Edge_Path("by.id") not in _.edges_by_path()

    def test_remove_edge_path_by_id__not_found(self):                           # Test removing nonexistent edge path
        with self.paths_index as _:
            _.remove_edge_path_by_id(Edge_Id(Obj_Id()))                                 # Should not crash

            assert _.edges_by_path() == {}

    # =========================================================================
    # Query Tests
    # =========================================================================

    def test_get_nodes_by_path__found(self):                                    # Test get_nodes_by_path
        node = Schema__MGraph__Node(node_path=Node_Path("query.path"))

        with self.paths_index as _:
            _.index_node_path(node)

            result = _.get_nodes_by_path(Node_Path("query.path"))

            assert node.node_id in result

    def test_get_nodes_by_path__not_found(self):                                # Test get_nodes_by_path with nonexistent path
        with self.paths_index as _:
            result = _.get_nodes_by_path(Node_Path("nonexistent"))

            assert result == set()

    def test_get_edges_by_path__found(self):                                    # Test get_edges_by_path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id = node1.node_id          ,
                                     to_node_id   = node2.node_id          ,
                                     edge_path    = Edge_Path("query.edge"))

        with self.paths_index as _:
            _.index_edge_path(edge)

            result = _.get_edges_by_path(Edge_Path("query.edge"))

            assert edge.edge_id in result

    def test_get_edges_by_path__not_found(self):                                # Test get_edges_by_path with nonexistent path
        with self.paths_index as _:
            result = _.get_edges_by_path(Edge_Path("nonexistent"))

            assert result == set()

    def test_get_all_node_paths(self):                                          # Test get_all_node_paths
        node1 = Schema__MGraph__Node(node_path=Node_Path("path.one"))
        node2 = Schema__MGraph__Node(node_path=Node_Path("path.two"))

        with self.paths_index as _:
            _.index_node_path(node1)
            _.index_node_path(node2)

            result = _.get_all_node_paths()

            assert Node_Path("path.one") in result
            assert Node_Path("path.two") in result
            assert len(result) == 2

    def test_get_all_edge_paths(self):                                          # Test get_all_edge_paths
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=Edge_Path("e.one"))
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=Edge_Path("e.two"))

        with self.paths_index as _:
            _.index_edge_path(edge1)
            _.index_edge_path(edge2)

            result = _.get_all_edge_paths()

            assert Edge_Path("e.one") in result
            assert Edge_Path("e.two") in result

    def test_get_node_path__found(self):                                        # Test get_node_path for specific node
        node = Schema__MGraph__Node(node_path=Node_Path("specific.path"))

        with self.paths_index as _:
            _.index_node_path(node)

            result = _.get_node_path(node.node_id)

            assert result == Node_Path("specific.path")

    def test_get_node_path__not_found(self):                                    # Test get_node_path for node without path
        with self.paths_index as _:
            result = _.get_node_path(Node_Id(Obj_Id()))

            assert result is None

    def test_get_edge_path__found(self):                                        # Test get_edge_path for specific edge
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=Edge_Path("found"))

        with self.paths_index as _:
            _.index_edge_path(edge)

            result = _.get_edge_path(edge.edge_id)

            assert result == Edge_Path("found")

    def test_get_edge_path__not_found(self):                                    # Test get_edge_path for edge without path
        with self.paths_index as _:
            result = _.get_edge_path(Edge_Id(Obj_Id()))

            assert result is None

    def test_count_nodes_by_path(self):                                         # Test count_nodes_by_path
        path  = Node_Path("counted")
        node1 = Schema__MGraph__Node(node_path=path)
        node2 = Schema__MGraph__Node(node_path=path)
        node3 = Schema__MGraph__Node(node_path=path)

        with self.paths_index as _:
            _.index_node_path(node1)
            _.index_node_path(node2)
            _.index_node_path(node3)

            assert _.count_nodes_by_path(path)                    == 3
            assert _.count_nodes_by_path(Node_Path("nonexistent")) == 0

    def test_count_edges_by_path(self):                                         # Test count_edges_by_path
        path  = Edge_Path("counted")
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge1 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=path)
        edge2 = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=path)

        with self.paths_index as _:
            _.index_edge_path(edge1)
            _.index_edge_path(edge2)

            assert _.count_edges_by_path(path)                    == 2
            assert _.count_edges_by_path(Edge_Path("nonexistent")) == 0

    def test_has_node_path(self):                                               # Test has_node_path
        node = Schema__MGraph__Node(node_path=Node_Path("exists"))

        with self.paths_index as _:
            _.index_node_path(node)

            assert _.has_node_path(Node_Path("exists"))     is True
            assert _.has_node_path(Node_Path("not_exists")) is False

    def test_has_edge_path(self):                                               # Test has_edge_path
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=Edge_Path("exists"))

        with self.paths_index as _:
            _.index_edge_path(edge)

            assert _.has_edge_path(Edge_Path("exists"))     is True
            assert _.has_edge_path(Edge_Path("not_exists")) is False

    # =========================================================================
    # Raw Accessor Tests
    # =========================================================================

    def test_nodes_by_path__accessor(self):                                     # Test raw accessor
        node = Schema__MGraph__Node(node_path=Node_Path("accessor"))

        with self.paths_index as _:
            _.index_node_path(node)

            result = _.nodes_by_path()

            assert type(result)              is not None
            assert Node_Path("accessor")     in result

    def test_edges_by_path__accessor(self):                                     # Test raw accessor
        node1 = Schema__MGraph__Node()
        node2 = Schema__MGraph__Node()
        edge  = Schema__MGraph__Edge(from_node_id=node1.node_id, to_node_id=node2.node_id, edge_path=Edge_Path("accessor"))

        with self.paths_index as _:
            _.index_edge_path(edge)

            result = _.edges_by_path()

            assert type(result)             is not None
            assert Edge_Path("accessor")    in result