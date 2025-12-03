from unittest                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class test_Domain__MGraph__Node(TestCase):

    def setUp(self):                                                                                  # Initialize test data
        self.node_data    = Schema__MGraph__Node__Data()
        self.schema_node  = Schema__MGraph__Node      (node_data = self.node_data  ,
                                                      node_type = Schema__MGraph__Node)
        self.model_node   = Model__MGraph__Node       (data      = self.schema_node)
        self.graph        = Model__MGraph__Graph      (                            )                  # Mock graph for testing
        self.node         = Domain__MGraph__Node      (node      = self.model_node,
                                                       graph     = self.graph     )
        self.graph.add_node(self.node.node.data)

    def test_init(self):                                                                             # Tests basic initialization
        assert type(self.node)         is Domain__MGraph__Node
        assert self.node.node          is self.model_node
        assert self.node.graph         is self.graph
        assert type(self.node.node_id) is Node_Id

    def test_add_node(self):                                                                         # Tests node addition functionality
        new_node_data    = Schema__MGraph__Node__Data()
        new_schema_node  = Schema__MGraph__Node      (node_data = new_node_data  ,
                                                     node_type = Schema__MGraph__Node)
        new_model_node   = Model__MGraph__Node       (data      = new_schema_node)

        self.node.add_node(new_model_node)

        # Verify the node was added to the graph
        added_node = self.graph.node(new_schema_node.node_id)
        assert added_node is not None
        assert added_node.data is new_schema_node

    def test_models__edges(self):                                                                    # Tests retrieving all connected edges
        node_1_id = self.graph.new_node().node_id
        # Create test edges
        edge_1        = Schema__MGraph__Edge        (from_node_id = self.node.node_id,
                                                     to_node_id   = node_1_id,
                                                     edge_type    = Schema__MGraph__Edge)

        edge_2        = Schema__MGraph__Edge        (from_node_id = node_1_id,
                                                     to_node_id   = self.node.node_id,
                                                     edge_type    = Schema__MGraph__Edge)

        # Add edges to graph
        self.graph.add_edge(edge_1)
        self.graph.add_edge(edge_2)

        # Test edge retrieval
        connected_edges = self.node.models__edges()
        assert len(connected_edges) == 2
        assert any(edge.edge_id() == edge_1.edge_id for edge in connected_edges)
        assert any(edge.edge_id() == edge_2.edge_id for edge in connected_edges)

    def test_models__from_edges(self):                                                               # Tests retrieving outgoing edges
        node_1_id = self.graph.new_node().node_id
        # Create test edges
        outgoing_edge = Schema__MGraph__Edge        (from_node_id = self.node.node_id,
                                                     to_node_id   = node_1_id,
                                                     edge_type    = Schema__MGraph__Edge)

        incoming_edge = Schema__MGraph__Edge        (from_node_id = node_1_id,
                                                     to_node_id   = self.node.node_id,
                                                     edge_type    = Schema__MGraph__Edge)

        # Add edges to graph
        self.graph.add_edge(outgoing_edge)
        self.graph.add_edge(incoming_edge)

        # Test outgoing edge retrieval
        outgoing_edges = self.node.models__from_edges()
        assert len(outgoing_edges) == 1
        assert outgoing_edges[0].edge_id() == outgoing_edge.edge_id

    def test_models__to_edges(self):                                                                 # Tests retrieving incoming edges
        node_1_id = self.graph.new_node().node_id
        # Create test edges
        outgoing_edge = Schema__MGraph__Edge        (from_node_id = self.node.node_id,
                                                     to_node_id   = node_1_id,
                                                     edge_type    = Schema__MGraph__Edge)

        incoming_edge = Schema__MGraph__Edge        (from_node_id = node_1_id,
                                                    to_node_id   = self.node.node_id,
                                                    edge_type    = Schema__MGraph__Edge)

        # Add edges to graph
        self.graph.add_edge(outgoing_edge)
        self.graph.add_edge(incoming_edge)

        # Test incoming edge retrieval
        incoming_edges = self.node.models__to_edges()
        assert len(incoming_edges) == 1
        assert incoming_edges[0].edge_id() == incoming_edge.edge_id

    def test_model__node_from_edge(self):                                                           # Tests retrieving connected nodes from edge
        # Create another node to connect to
        other_node_data   = Schema__MGraph__Node__Data()
        other_schema_node = Schema__MGraph__Node      (node_data = other_node_data,
                                                      node_type = Schema__MGraph__Node)
        other_model_node  = Model__MGraph__Node       (data      = other_schema_node)
        self.graph.add_node(other_schema_node)

        # Create edge connecting nodes
        edge        = Schema__MGraph__Edge        (from_node_id = self.node.node_id,
                                                  to_node_id   = other_schema_node.node_id,
                                                  edge_type    = Schema__MGraph__Edge)
        model_edge  = Model__MGraph__Edge         (data        = edge)
        self.graph.add_edge(edge)

        # Test getting connected node from outgoing edge
        connected_node = self.node.model__node_from_edge(model_edge)
        assert connected_node is not None
        assert connected_node.data is other_schema_node

        # Test getting connected node from incoming edge
        edge.from_node_id = other_schema_node.node_id
        edge.to_node_id = self.node.node_id
        connected_node = self.node.model__node_from_edge(model_edge)
        assert connected_node is not None
        assert connected_node.data is other_schema_node

        # Test with unconnected edge
        edge.from_node_id = Node_Id(Obj_Id())
        edge.to_node_id   = Node_Id(Obj_Id())
        assert self.node.model__node_from_edge(model_edge) is None