from types                                                   import NoneType
from unittest                                                import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Edge            import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node            import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Edge             import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node             import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Types          import Schema__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node           import Schema__MGraph__Node
from mgraph_db.mgraph.MGraph                                 import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph           import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph            import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph          import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data    import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.utils.MGraph__Random_Graph             import MGraph__Random_Graph, create_empty_mgraph, create_random_mgraph


class test_MGraph__Random_Graph(TestCase):

    def setUp(self):                                                                # Setup test instance
        self.random_graph = MGraph__Random_Graph().setup()

    def test_init(self):                                                           # Test initialization
        assert type(self.random_graph                   ) is MGraph__Random_Graph
        assert type(self.random_graph.graph             ) is MGraph
        assert type(self.random_graph.graph__graph      ) is Domain__MGraph__Graph
        assert type(self.random_graph.graph__model      ) is Model__MGraph__Graph
        assert type(self.random_graph.graph__schema     ) is Schema__MGraph__Graph
        assert type(self.random_graph.graph__data       ) is Schema__MGraph__Graph__Data
        assert len(self.random_graph.graph__schema.nodes) == 0
        assert len(self.random_graph.graph__schema.edges) == 0

    def test_create_nodes(self):                                                   # Test node creation
        num_nodes = 5
        node_ids = self.random_graph.create_nodes(num_nodes)

        assert len(node_ids)                               == num_nodes
        assert len(self.random_graph.graph__schema.nodes) == num_nodes

        for node_id in node_ids:                                                   # Verify each node exists
            node = self.random_graph.graph.data().node(node_id)
            assert node is not None

    def test_create_nodes_validation(self):                                        # Test node creation validation
        with self.assertRaises(ValueError) as context:
            self.random_graph.create_nodes(-1)
        assert str(context.exception) == "Number of nodes cannot be negative"

    def test_create_random_edges(self):                                           # Test edge creation
        num_nodes = 5
        num_edges = 10
        node_ids = self.random_graph.create_nodes(num_nodes)

        self.random_graph.create_random_edges(node_ids, num_edges)
        assert len(self.random_graph.graph__schema.edges) == num_edges

        for edge in self.random_graph.graph.data().edges():                       # Verify each edge connects existing nodes
            assert edge.from_node() is not None
            assert edge.to_node() is not None

    def test_create_random_edges_validation(self):                                # Test edge creation validation
        with self.assertRaises(ValueError) as context:
            self.random_graph.create_random_edges([], 5)
        assert str(context.exception) == "No nodes available to create edges"

        node_ids = self.random_graph.create_nodes(5)
        with self.assertRaises(ValueError) as context:
            self.random_graph.create_random_edges(node_ids, -1)
        assert str(context.exception) == "Number of edges cannot be negative"

    def test_create_graph_default_params(self):                                   # Test graph creation with defaults
        graph = self.random_graph.create_random_graph()

        assert len(graph.data().nodes()) == 10                                    # Default 10 nodes
        assert len(graph.data().edges()) == 20                                    # Default 20 edges (2x nodes)

    def test_create_graph_custom_params(self):                                    # Test graph creation with custom params
        num_nodes = 5
        num_edges = 7
        graph = self.random_graph.create_random_graph(num_nodes=num_nodes, num_edges=num_edges)
        assert len(graph.data().nodes()) == num_nodes
        assert len(graph.data().edges()) == num_edges

    def test_create_empty_mgraph(self):                                           # Test empty graph creation
        mgraph = create_empty_mgraph()
        assert type(mgraph)                   is MGraph
        assert len (mgraph.data().nodes())    == 0
        assert len (mgraph.data().edges())    == 0
        assert type(mgraph.graph            ) is Domain__MGraph__Graph
        assert type(mgraph.graph.model      ) is Model__MGraph__Graph
        assert type(mgraph.graph.model.data ) is Schema__MGraph__Graph


    def test_multiple_graph_creation(self):                                      # Test creating multiple graphs
        graph1 = create_random_mgraph(num_nodes=3, num_edges=5)
        assert len(graph1.data().nodes()) == 3
        assert len(graph1.data().edges()) == 5

        graph2 = create_random_mgraph(num_nodes=4, num_edges=6)
        assert len(graph2.data().nodes()) == 4
        assert len(graph2.data().edges()) == 6

    def test_create_random_mgraph(self):
        with create_random_mgraph() as _:
            assert type(_                        ) is MGraph
            assert type(_.graph                  ) is Domain__MGraph__Graph
            assert type(_.graph.model            ) is Model__MGraph__Graph
            assert type(_.graph.model.data       ) is Schema__MGraph__Graph
            assert len(_.graph           .nodes()) == 2
            assert len(_.graph.model     .nodes()) == 2
            assert len(_.graph.model.data.nodes  ) == 2
            assert len(_.graph           .edges()) == 2
            assert len(_.graph.model     .edges()) == 2
            assert len(_.graph.model.data.edges  ) == 2

            domain_node = _.graph.nodes                       () [0]
            model_node  = _.graph.model.nodes                 () [0]
            schema_node = list(_.graph.model.data.nodes.values())[0]

            assert type(domain_node                                ) == Domain__MGraph__Node
            assert type(domain_node.node                           ) == Model__MGraph__Node
            assert type(domain_node.graph                          ) == Model__MGraph__Graph
            assert type(domain_node.graph.data                     ) == Schema__MGraph__Graph
            assert type(domain_node.graph.data.schema_types)         == Schema__MGraph__Types
            assert domain_node.graph.model_types.node_model_type     is  None

            assert type(model_node                 ) == Model__MGraph__Node
            assert type(model_node.data            ) == Schema__MGraph__Node

            assert type(schema_node                ) == Schema__MGraph__Node
            assert type(schema_node.node_data)       is NoneType


            domain_edge = _.graph.edges                       () [0]
            model_edge  = _.graph.model.edges                 () [0]
            schema_edge = list(_.graph.model.data.edges.values())[0]

            assert type(domain_edge                               ) == Domain__MGraph__Edge
            assert type(domain_edge.edge                          ) == Model__MGraph__Edge
            assert type(domain_edge.graph                         ) == Model__MGraph__Graph
            assert type(domain_edge.graph.data                    ) == Schema__MGraph__Graph
            assert type(domain_edge.graph.data.schema_types)        == Schema__MGraph__Types
            assert domain_edge.graph.model_types.edge_model_type    is None

            assert type(model_edge           ) == Model__MGraph__Edge
            assert type(model_edge.data      ) == Schema__MGraph__Edge
            assert type(schema_node          ) == Schema__MGraph__Node
            assert type(schema_node.node_data) is NoneType
            assert type(schema_edge          ) == Schema__MGraph__Edge





