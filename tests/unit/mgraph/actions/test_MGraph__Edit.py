from unittest                                                    import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Node                import Domain__MGraph__Node
from osbot_utils.testing.__                                      import __
from mgraph_db.mgraph.actions.MGraph__Edit                       import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Graph               import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph                import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph              import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node               import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import is_obj_id


class Simple_Node(Schema__MGraph__Node): pass  # Helper class for testing

class test_MGraph__Edit(TestCase):

    def setUp(self):
        self.schema_graph = Schema__MGraph__Graph ( nodes      = {}                     ,
                                                    edges      = {}                     ,
                                                    graph_type = Schema__MGraph__Graph  )                               # Create a schema graph
        self.model_graph  = Model__MGraph__Graph  ( data       = self.schema_graph      )                               # Create model and domain graph
        self.domain_graph = Domain__MGraph__Graph ( model      = self.model_graph       )
        self.graph_edit   = MGraph__Edit          ( graph      = self.domain_graph      )                               # Create edit object

    def test_add_node(self):
        with self.graph_edit as _:
            node    = _.new_node()
            node_id = node.node_id
            assert type(node)         is Domain__MGraph__Node
            assert is_obj_id(node_id) is True
            assert node.obj()         == __(node=__(data=__(node_data   = __()    ,
                                                            node_id     = node_id ,
                                                            node_type   = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node')),
                                            graph=self.model_graph.obj())
            assert node.node.json() == self.model_graph.node(node_id=node_id).json()

    def test_new_node(self):
        node = self.graph_edit.new_node()                                                                         # Create a simple node
        assert type(node) is Domain__MGraph__Node

    def test_new_edge(self):
        node_1 = self.graph_edit.new_node()                                                                             # Create two nodes
        node_2 = self.graph_edit.new_node()
        edge  = self.graph_edit.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)                                                              # Create edge between nodes

        assert edge is not None
        assert edge.from_node().node_id == node_1.node_id
        assert edge.to_node  ().node_id == node_2.node_id

    def test_deletion(self):
        with self.graph_edit as _:
            node_1 = _.new_node()                                # Create 3x nodes and 2x edges
            node_2 = _.new_node()
            node_3 = _.new_node()
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            assert _.delete_node(node_1.node_id) is True                       # Test node deletion
            assert _.delete_node(node_1.node_id) is False
            assert _.graph.node (node_1.node_id) is None
            assert _.graph.edge (edge_1.edge_id) is None

            assert _.delete_edge(edge_2.edge_id) is True                       # Test edge deletion
            assert _.delete_edge(edge_2.edge_id) is False
            assert _.graph.edge (edge_2.edge_id) is None

    def test_node_with_custom_type(self):
        class Custom_Node(Schema__MGraph__Node): pass
        custom_node = Custom_Node()

        assert custom_node.obj() == __(node_id   = custom_node.node_id,
                                       node_data = __(),
                                       node_type = 'test_MGraph__Edit.Custom_Node')

        node = self.graph_edit.new_node(node_type=Custom_Node)     # Create node with custom type

        assert node.node.data.node_type is Custom_Node