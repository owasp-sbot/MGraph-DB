from unittest                                                       import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data

class test_Domain__MGraph__Edge(TestCase):

    def setUp(self):                                                                                    # Initialize test data
        self.graph            = Model__MGraph__Graph       ( data=None)                                # Mock graph for testing
        self.from_node_data   = Schema__MGraph__Node__Data (          )                                # Create source and target nodes
        self.from_schema_node = Schema__MGraph__Node       ( node_data = self.from_node_data ,
                                                             node_type = Schema__MGraph__Node)
        self.to_node_data     = Schema__MGraph__Node__Data (         )
        self.to_schema_node   = Schema__MGraph__Node       ( node_data = self.to_node_data   ,
                                                             node_type = Schema__MGraph__Node)

        # Add nodes to the graph
        self.graph.data = Schema__MGraph__Graph(nodes        = {self.from_schema_node.node_id: self.from_schema_node,
                                                                self.to_schema_node.node_id  : self.to_schema_node},
                                                graph_type   = Schema__MGraph__Graph)

        # Create edge configuration and schema
        self.schema_edge = Schema__MGraph__Edge        (edge_type      = Schema__MGraph__Edge,
                                                        from_node_id   = self.from_schema_node.node_id,
                                                        to_node_id     = self.to_schema_node.node_id)

        # Create model and domain edge
        self.model_edge = Model__MGraph__Edge(data=self.schema_edge)
        self.edge       = Domain__MGraph__Edge(edge=self.model_edge, graph=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.edge)           is Domain__MGraph__Edge
        assert self.edge.edge            is self.model_edge
        assert self.edge.graph           is self.graph
        assert type(self.edge.edge_id)   is Edge_Id

    def test_node_operations(self):                                                         # Tests from_node and to_node methods
        from_node = self.edge.from_node()
        to_node   = self.edge.to_node  ()
        assert type(from_node) is Domain__MGraph__Node
        assert type(to_node)   is Domain__MGraph__Node