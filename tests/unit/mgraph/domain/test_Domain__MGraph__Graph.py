from unittest                                            import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Types      import Schema__MGraph__Types
from mgraph_db.mgraph.domain.Domain__MGraph__Edge        import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node        import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Node         import Model__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Graph       import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph        import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph      import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node

class Simple_Node(Schema__MGraph__Node): pass                                                   # Helper class for testing

class test_Domain__MGraph__Graph(TestCase):

    def setUp(self):                                                                            # Initialize test data
        self.schema_types = Schema__MGraph__Types  (node_type       = Simple_Node,
                                                    node_data_type  = Schema__MGraph__Node__Data,
                                                    edge_type       = None)
        self.schema_graph = Schema__MGraph__Graph           (schema_types = self.schema_types    ,
                                                             graph_type   = Schema__MGraph__Graph)
        self.model_graph = Model__MGraph__Graph             (data         = self.schema_graph    )                         # Create model graph
        self.graph       = Domain__MGraph__Graph            (model        = self.model_graph     )

    def test_init(self):                                                                        # Tests basic initialization
        assert type(self.graph) is Domain__MGraph__Graph
        assert self.graph.model   is self.model_graph

    def test_node_operations(self):                                                             # Tests node creation and management

        node = self.graph.new_node()                                          # Create a node

        assert node                 is not None                                                 # Verify node creatio
        assert type(node          ) is Domain__MGraph__Node
        assert type(node.node     ) is Model__MGraph__Node
        assert type(node.node.data) is Simple_Node
        retrieved_node = self.graph.node(node.node_id)                                             # Retrieve node by ID
        assert retrieved_node         is not None

        assert type(retrieved_node) is Domain__MGraph__Node

        # List all nodes
        nodes = self.graph.nodes()
        assert len(nodes)       == 1
        assert nodes[0].json()  == retrieved_node.json()

        # Delete node
        assert self.graph.delete_node(node.node_id) is True
        assert self.graph.node       (node.node_id) is None

    def test_edge_operations(self):                                                             # Tests edge creation and management
        node1          = self.graph.new_node()                                        # Create nodes for edge
        node2          = self.graph.new_node()
        edge           = self.graph.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)                             # Create an edge
        from_node      = edge.from_node()
        to_node        = edge.to_node  ()
        retrieved_edge = self.graph.edge(edge.edge_id)                                                  # Retrieve edge by ID

        assert edge                  is not None                                                        # Verify edge creation
        assert type(from_node      ) is Domain__MGraph__Node
        assert type(to_node        ) is Domain__MGraph__Node
        assert type(from_node.graph) is Model__MGraph__Graph
        assert type(to_node  .graph) is Model__MGraph__Graph

        assert retrieved_edge             is not None
        assert type(retrieved_edge      ) is Domain__MGraph__Edge
        assert type(retrieved_edge.graph) is Model__MGraph__Graph


        edges = self.graph.edges()                                                              # List all edges
        assert len(edges)                        == 1
        assert edges[0].json()                   == retrieved_edge.json()

        assert self.graph.delete_edge(edge.edge_id) is True                                        # Delete edge
        assert self.graph.edge       (edge.edge_id) is None

    def test_node_with_custom_type(self):                                                   # Test creating nodes with custom types
        class CustomNode(Simple_Node): pass

        node = self.graph.new_node(node_type=CustomNode)                    # Create node with custom type
        assert node.node.data.node_type is CustomNode

    def test_graph_state_persistence(self):                                                 # Test graph state persistence
        node1 = self.graph.new_node()                                                # Create nodes and edge
        node2 = self.graph.new_node()
        edge  = self.graph.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

        assert type(edge) == Domain__MGraph__Edge
        assert len(self.graph.nodes())            == 2                                      # Verify multiple graph queries
        assert len(self.graph.edges())            == 1
        assert self.graph.delete_node(node1.node_id) is True                                   # Delete operations
        assert len(self.graph.nodes())            == 1
        assert len(self.graph.edges())            == 0