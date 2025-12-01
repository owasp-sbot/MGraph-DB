from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from mgraph_db.mgraph.utils.MGraph__Random_Graph                    import create_empty_mgraph
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class test_MGraph__Index__paths(TestCase):

    def setUp(self):
        self.mgraph = create_empty_mgraph()

    def test_index_nodes_by_path(self):                                                             # Test path-based node indexing
        with self.mgraph.edit() as _:
            node1 = _.new_node(node_path=Node_Path("html.body"    ))
            node2 = _.new_node(node_path=Node_Path("html.body.div"))
            node3 = _.new_node(node_path=Node_Path("html.head"    ))
            node4 = _.new_node()                                                                    # No path

        with self.mgraph.index() as _:
            body_nodes = _.get_nodes_by_path(Node_Path("html.body"))                                # Exact match - returns set of node_ids
            assert node1.node_id in body_nodes
            assert len(body_nodes) == 1

            div_nodes = _.get_nodes_by_path(Node_Path("html.body.div"))
            assert node2.node_id in div_nodes
            assert len(div_nodes) == 1

            head_nodes = _.get_nodes_by_path(Node_Path("html.head"))
            assert node3.node_id in head_nodes
            assert len(head_nodes) == 1

            nonexistent = _.get_nodes_by_path(Node_Path("nonexistent"))                             # Non-existent path returns empty set
            assert len(nonexistent) == 0

            all_path_node_ids = set()                                                               # Node without path is not in any path index
            for node_ids in _.nodes_by_path().values():
                all_path_node_ids.update(node_ids)
            assert node4.node_id not in all_path_node_ids

    def test_multiple_nodes_same_path(self):                                                        # Test that multiple nodes can share the same path
        with self.mgraph.edit() as _:
            node1 = _.new_node(node_path=Node_Path("article.paragraph"))
            node2 = _.new_node(node_path=Node_Path("article.paragraph"))
            node3 = _.new_node(node_path=Node_Path("article.paragraph"))

        with self.mgraph.index() as _:
            paragraph_nodes = _.get_nodes_by_path(Node_Path("article.paragraph"))

            assert node1.node_id in paragraph_nodes
            assert node2.node_id in paragraph_nodes
            assert node3.node_id in paragraph_nodes
            assert len(paragraph_nodes) == 3

    def test_index_edges_by_path(self):                                                             # Test path-based edge indexing
        with self.mgraph.edit() as _:
            node1 = _.new_node()
            node2 = _.new_node()
            node3 = _.new_node()

            edge1 = _.new_edge( from_node_id = node1.node_id                        ,
                                to_node_id   = node2.node_id                        ,
                                edge_path    = Edge_Path("relationship.contains")   )
            edge2 = _.new_edge( from_node_id = node2.node_id                        ,
                                to_node_id   = node3.node_id                        ,
                                edge_path    = Edge_Path("relationship.references") )
            edge3 = _.new_edge( from_node_id = node1.node_id                        ,
                                to_node_id   = node3.node_id                        )               # No path

        with self.mgraph.index() as _:
            contains_edges = _.get_edges_by_path(Edge_Path("relationship.contains"))
            assert edge1.edge_id in contains_edges
            assert len(contains_edges) == 1

            references_edges = _.get_edges_by_path(Edge_Path("relationship.references"))
            assert edge2.edge_id in references_edges
            assert len(references_edges) == 1

            nonexistent = _.get_edges_by_path(Edge_Path("nonexistent"))
            assert len(nonexistent) == 0

    def test_multiple_edges_same_path(self):                                                        # Test that multiple edges can share the same path
        with self.mgraph.edit() as _:
            node1 = _.new_node()
            node2 = _.new_node()
            node3 = _.new_node()

            edge1 = _.new_edge( from_node_id = node1.node_id            ,
                                to_node_id   = node2.node_id            ,
                                edge_path    = Edge_Path("parent.child"))
            edge2 = _.new_edge( from_node_id = node1.node_id            ,
                                to_node_id   = node3.node_id            ,
                                edge_path    = Edge_Path("parent.child"))
            edge3 = _.new_edge( from_node_id = node2.node_id            ,
                                to_node_id   = node3.node_id            ,
                                edge_path    = Edge_Path("parent.child"))

        with self.mgraph.index() as _:
            parent_child_edges = _.get_edges_by_path(Edge_Path("parent.child"))

            assert edge1.edge_id in parent_child_edges
            assert edge2.edge_id in parent_child_edges
            assert edge3.edge_id in parent_child_edges
            assert len(parent_child_edges) == 3

            assert parent_child_edges == _.get_edges_by_path("parent.child")            # direct fetch also works  (i.e. without using Edge_Path)


    #class test_MGraph__Edit__paths(TestCase):

    def test_set_node_path(self):                                                                   # Test setting/updating a node's path
        with self.mgraph.edit() as _:
            node    = _.new_node()
            node_id = node.node_id

            assert node.node.data.node_path is None                                                 # Initially no path
            assert len(_.index().get_nodes_by_path(Node_Path("new.path"))) == 0

            result = _.set_node_path(node_id, Node_Path("new.path"))                                # Set path
            assert result is True

            updated_node = _.data().node(node_id)                                                   # Verify path is set and indexed
            assert updated_node.node.data.node_path == Node_Path("new.path")
            assert node_id in _.index().get_nodes_by_path(Node_Path("new.path"))

    def test_update_node_path(self):                                                                # Test updating an existing node's path
        with self.mgraph.edit() as _:
            node    = _.new_node(node_path=Node_Path("old.path"))
            node_id = node.node_id

            assert node_id in _.index().get_nodes_by_path(Node_Path("old.path"))                    # Verify initial path

            result = _.set_node_path(node_id, Node_Path("new.path"))                                # Update path
            assert result is True

            assert node_id not in _.index().get_nodes_by_path(Node_Path("old.path"))                # Verify old path removed, new path added
            assert node_id     in _.index().get_nodes_by_path(Node_Path("new.path"))

    def test_clear_node_path(self):                                                                 # Test clearing a node's path by setting to None
        with self.mgraph.edit() as _:
            node    = _.new_node(node_path=Node_Path("existing.path"))
            node_id = node.node_id

            assert node_id in _.index().get_nodes_by_path(Node_Path("existing.path"))               # Verify initial path

            result = _.set_node_path(node_id, '')                                                   # Clear path
            assert result is True

            updated_node = _.data().node(node_id)                                                   # Verify path cleared and index updated
            assert updated_node.node.data.node_path == ''
            assert node_id not in _.index().get_nodes_by_path(Node_Path("existing.path"))

    def test_set_edge_path(self):                                                                   # Test setting/updating an edge's path
        with self.mgraph.edit() as _:
            node1   = _.new_node()
            node2   = _.new_node()
            edge    = _.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
            edge_id = edge.edge_id

            assert edge.edge.data.edge_path is None                                                 # Initially no path

            result = _.set_edge_path(edge_id, Edge_Path("new.edge.path"))                           # Set path
            assert result is True

            updated_edge = _.data().edge(edge_id)                                                   # Verify path is set and indexed
            assert updated_edge.edge.data.edge_path == Edge_Path("new.edge.path")
            assert edge_id in _.index().get_edges_by_path(Edge_Path("new.edge.path"))

    def test_update_edge_path(self):                                                                # Test updating an existing edge's path
        with self.mgraph.edit() as _:
            node1   = _.new_node()
            node2   = _.new_node()
            edge    = _.new_edge( from_node_id = node1.node_id         ,
                                  to_node_id   = node2.node_id         ,
                                  edge_path    = Edge_Path("old.path") )
            edge_id = edge.edge_id

            assert edge_id in _.index().get_edges_by_path(Edge_Path("old.path"))                    # Verify initial path

            result = _.set_edge_path(edge_id, Edge_Path("new.path"))                                # Update path
            assert result is True

            assert edge_id not in _.index().get_edges_by_path(Edge_Path("old.path"))                # Verify old path removed, new path added
            assert edge_id     in _.index().get_edges_by_path(Edge_Path("new.path"))

    def test_set_path_nonexistent_node(self):                                                       # Test that setting path on nonexistent node returns False
        with self.mgraph.edit() as _:
            fake_node_id = Node_Id()
            result       = _.set_node_path(fake_node_id, Node_Path("some.path"))
            assert result is False

    def test_set_path_nonexistent_edge(self):                                                       # Test that setting path on nonexistent edge returns False
        with self.mgraph.edit() as _:
            fake_edge_id = Edge_Id()
            result       = _.set_edge_path(fake_edge_id, Edge_Path("some.path"))
            assert result is False


    #class test_MGraph__Index__path_removal(TestCase):


    def test_delete_node_removes_from_path_index(self):                                             # Test that deleting a node removes it from the path index
        with self.mgraph.edit() as _:
            node    = _.new_node(node_path=Node_Path("to.be.deleted"))
            node_id = node.node_id

            assert node_id in _.index().get_nodes_by_path(Node_Path("to.be.deleted"))               # Verify node is in path index

            result = _.delete_node(node_id)                                                         # Delete node
            assert result is True

            assert node_id not in _.index().get_nodes_by_path(Node_Path("to.be.deleted"))           # Verify removed from path index

    def test_delete_edge_removes_from_path_index(self):                                             # Test that deleting an edge removes it from the path index
        with self.mgraph.edit() as _:
            node1   = _.new_node()
            node2   = _.new_node()
            edge    = _.new_edge( from_node_id = node1.node_id                ,
                                  to_node_id   = node2.node_id                ,
                                  edge_path    = Edge_Path("to.be.deleted")   )
            edge_id = edge.edge_id

            assert edge_id in _.index().get_edges_by_path(Edge_Path("to.be.deleted"))               # Verify edge is in path index

            result = _.delete_edge(edge_id)                                                         # Delete edge
            assert result is True

            assert edge_id not in _.index().get_edges_by_path(Edge_Path("to.be.deleted"))           # Verify removed from path index


    #class test_MGraph__Index__stats_with_paths(TestCase):


    def test_stats_include_path_counts(self):                                                       # Test that stats() includes path-based statistics
        with self.mgraph.edit() as _:
            _.new_node(node_path=Node_Path("path.one"))
            _.new_node(node_path=Node_Path("path.one"))
            _.new_node(node_path=Node_Path("path.two"))
            _.new_node()                                                                            # No path

            node1 = _.new_node()
            node2 = _.new_node()
            _.new_edge( from_node_id = node1.node_id          ,
                        to_node_id   = node2.node_id          ,
                        edge_path    = Edge_Path("edge.path") )

        stats = self.mgraph.index().stats()

        assert 'nodes_by_path' in stats['index_data']
        assert 'edges_by_path' in stats['index_data']

        nodes_by_path = stats['index_data']['nodes_by_path']                                        # Check node path counts
        assert nodes_by_path.get('path.one') == 2
        assert nodes_by_path.get('path.two') == 1

        edges_by_path = stats['index_data']['edges_by_path']                                        # Check edge path counts
        assert edges_by_path.get('edge.path') == 1