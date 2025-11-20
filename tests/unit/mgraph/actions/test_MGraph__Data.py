from unittest                                                       import TestCase
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class Simple_Node(Schema__MGraph__Node): pass  # Helper class for testing

class test_MGraph__Data(TestCase):

    def setUp(self):
        schema_graph = Schema__MGraph__Graph(graph_type=Schema__MGraph__Graph)   # Create a schema graph

        model_graph  = Model__MGraph__Graph(data=schema_graph)                                                          # Create model and domain graph
        domain_graph = Domain__MGraph__Graph(model=model_graph)
        self.graph_data    = MGraph__Data(graph=domain_graph)                                                                 # Create data object

    def test_node_and_edge_retrieval(self):
        node1           = self.graph_data.graph.new_node()                                                              # Create nodes and edges
        node2           = self.graph_data.graph.new_node()
        edge            = self.graph_data.graph.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
        retrieved_node = self.graph_data.node(node1.node_id)                                                                # Test node retrieval

        assert retrieved_node         is not None

        retrieved_edge = self.graph_data.edge(edge.edge_id)                                                                 # Test edge retrieval
        assert self.graph_data.edges()[0].json()  == edge.json()
        assert self.graph_data.nodes()[0].json()  == node1.json()
        assert self.graph_data.nodes()[1].json()  == node2.json()
        assert retrieved_edge                     is not None

    def test_list_nodes_and_edges(self):
        node1 = self.graph_data.graph.new_node()                                                                       # Create multiple nodes and edges
        node2 = self.graph_data.graph.new_node()
        edge  = self.graph_data.graph.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
        nodes = self.graph_data.graph.nodes()                                                                                 # get nodes list
        edges = self.graph_data.graph.edges()                                                                                 # get edges list

        assert len(nodes)   == 2
        assert node1.json() == nodes[0].json()
        assert node2.json() == nodes[1].json()
        assert len(edges)   == 1
        assert edge.json()  == edges[0].json()

    def test_nonexistent_retrieval(self):
        non_existent_id = Obj_Id()                                                                                 # Test retrieving non-existent node and edge
        assert self.graph_data.node(non_existent_id) is None
        assert self.graph_data.edge(non_existent_id) is None
