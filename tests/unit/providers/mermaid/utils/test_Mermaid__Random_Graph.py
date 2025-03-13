from unittest                                                            import TestCase
from mgraph_db.providers.mermaid.MGraph__Mermaid                         import MGraph__Mermaid
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge            import Domain__Mermaid__Edge
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph           import Domain__Mermaid__Graph
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node            import Domain__Mermaid__Node
from mgraph_db.providers.mermaid.models.Model__Mermaid__Edge             import Model__Mermaid__Edge
from mgraph_db.providers.mermaid.models.Model__Mermaid__Graph            import Model__Mermaid__Graph
from mgraph_db.providers.mermaid.models.Model__Mermaid__Node             import Model__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types          import Schema__Mermaid__Types
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data     import Schema__Mermaid__Node__Data
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config
from mgraph_db.providers.mermaid.utils.Mermaid__Random_Graph             import Mermaid__Random_Graph, create_test_mermaid_graph, create_empty_mermaid_graph
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.type_safe.Type_Safe__List                               import Type_Safe__List


class test_Test_Data_Mermaid(TestCase):

    def setUp(self):                                                                    # Initialize test instance
        self.test_data = Mermaid__Random_Graph()
        self.test_data.setup()

    def test_init(self):                                                               # Test initialization
        assert type(self.test_data)                         is Mermaid__Random_Graph
        assert type(self.test_data.graph_data)              is Schema__Mermaid__Graph
        assert type(self.test_data.graph__model)            is Model__Mermaid__Graph
        assert len(self.test_data.graph_data.nodes)         == 0
        assert len(self.test_data.graph_data.edges)         == 0
        assert type(self.test_data.graph_data.mermaid_code) is Type_Safe__List
        assert len(self.test_data.graph_data .mermaid_code)  == 0

    def test_create_mermaid_node(self):                                                # Test Mermaid node creation
        key = "test_key"
        label = "Test Label"

        # Test with all parameters
        node = self.test_data.create_mermaid_node(key=key, label=label)
        assert type(node)           is Schema__Mermaid__Node
        assert type(node.node_data) is Schema__Mermaid__Node__Data
        assert node.key             == Safe_Id(key)
        assert node.label           == label

        # Test with default parameters
        node = self.test_data.create_mermaid_node(key=key)
        assert node.key                   == Safe_Id(key)
        assert node.label                 == f"Label {Safe_Id(key)}"

    def test_create_mermaid_edge(self):                                                # Test Mermaid edge creation
        node1 = self.test_data.create_mermaid_node(key="node1")
        node2 = self.test_data.create_mermaid_node(key="node2")
        label = "Test Edge"

        # Test with explicit label
        edge = self.test_data.create_mermaid_edge(from_node=node1, to_node=node2, label=label)
        assert type(edge)                  is Schema__Mermaid__Edge
        assert type(edge.edge_config)      is Schema__Mermaid__Edge__Config
        assert edge.from_node_id           == node1.node_id
        assert edge.to_node_id             == node2.node_id
        assert edge.label                  == label

        # Test with default label
        edge = self.test_data.create_mermaid_edge(from_node=node1, to_node=node2)
        assert edge.label == f"Edge {node1.key} to {node2.key}"

    def test_create_nodes(self):                                                       # Test node creation
        num_nodes = 5
        nodes = self.test_data.create_nodes(num_nodes)

        assert len(nodes) == num_nodes
        assert len(self.test_data.graph_data.nodes) == num_nodes

        for i, node in enumerate(nodes):
            assert type(node) is Schema__Mermaid__Node
            assert node.key == Safe_Id(f'key_{i}')

        # Test validation
        with self.assertRaises(ValueError) as context:
            self.test_data.create_nodes(-1)
        assert str(context.exception) == "Number of nodes cannot be negative"

    def test_create_random_edges(self):                                               # Test random edge creation
        nodes = self.test_data.create_nodes(5)
        num_edges = 10

        self.test_data.create_random_edges(nodes, num_edges)
        assert len(self.test_data.graph_data.edges) == num_edges

        for edge in self.test_data.graph_data.edges.values():
            assert type(edge) is Schema__Mermaid__Edge
            assert edge.from_node_id in [node.node_id for node in nodes]
            assert edge.to_node_id in [node.node_id for node in nodes]

        # Test validation
        with self.assertRaises(ValueError) as context:
            self.test_data.create_random_edges([], 5)
        assert str(context.exception) == "No nodes available to create edges"

        with self.assertRaises(ValueError) as context:
            self.test_data.create_random_edges(nodes, -1)
        assert str(context.exception) == "Number of edges cannot be negative"

    def test_create_test_graph(self):                                                 # Test complete graph creation
        num_nodes = 5
        num_edges = 8

        # Test with explicit edge count
        graph = Mermaid__Random_Graph().setup().create_test_graph(num_nodes=num_nodes, num_edges=num_edges)
        model = graph.graph.model
        assert type(graph) is MGraph__Mermaid
        assert type(model) is Model__Mermaid__Graph

        assert len(model.data.nodes) == num_nodes
        assert len(model.data.edges) == num_edges

        # Test with default edge count
        graph = Mermaid__Random_Graph().setup().create_test_graph(num_nodes=num_nodes)
        model = graph.graph.model
        assert len(model.data.nodes) == num_nodes
        assert len(model.data.edges) == num_nodes * 2

    def test_helper_functions(self):                                                   # Test static helper functions
        # Test create_test_mermaid_graph
        graph = create_test_mermaid_graph(num_nodes=3, num_edges=5)
        model = graph.graph.model
        assert type(graph) is MGraph__Mermaid
        assert len(model.data.nodes) == 3
        assert len(model.data.edges) == 5

        # Test create_empty_mermaid_graph
        empty_graph = create_empty_mermaid_graph()
        model       = empty_graph.graph.model
        assert type(empty_graph) is MGraph__Mermaid
        assert len(model.data.nodes) == 0
        assert len(model.data.edges) == 0

    def test_edge_cases(self):                                                        # Test edge cases
        # Test zero nodes
        graph = create_test_mermaid_graph(num_nodes=1, num_edges=1)
        model = graph.graph.model
        assert len(model.data.nodes) == 1
        assert len(model.data.edges) == 1

        # Test zero edges
        graph = create_test_mermaid_graph(num_nodes=5, num_edges=0)
        model = graph.graph.model
        assert len(model.data.nodes) == 5
        assert len(model.data.edges) == 0

        # Test large numbers
        large_num = 100
        graph = create_test_mermaid_graph(num_nodes=large_num, num_edges=large_num)
        model = graph.graph.model
        assert len(model.data.nodes) == large_num
        assert len(model.data.edges) == large_num

    def test_node_and_edge_consistency(self):                                         # Test data consistency
        num_nodes = 5
        num_edges = 10
        graph = self.test_data.create_test_graph(num_nodes=num_nodes, num_edges=num_edges)
        model = graph.graph.model

        # Check node properties
        for node in model.data.nodes.values():
            assert type(node) is Schema__Mermaid__Node
            assert node.key is not None
            assert node.label is not None

        # Check edge properties
        for edge in model.data.edges.values():
            assert type(edge) is Schema__Mermaid__Edge
            assert edge.label is not None
            # Verify edge endpoints exist
            assert edge.from_node_id in model.data.nodes
            assert edge.to_node_id   in model.data.nodes

    def test_create_random_mgraph(self):
        with create_test_mermaid_graph() as _:

            assert type(_                        ) is MGraph__Mermaid
            assert type(_.graph                  ) is Domain__Mermaid__Graph
            assert type(_.graph.model            ) is Model__Mermaid__Graph
            assert type(_.graph.model.data       ) is Schema__Mermaid__Graph

            assert len(_.graph           .nodes()) == 2
            assert len(_.graph.model     .nodes()) == 2
            assert len(_.graph.model.data.nodes  ) == 2
            assert len(_.graph           .edges()) == 2
            assert len(_.graph.model     .edges()) == 2
            assert len(_.graph.model.data.edges  ) == 2

            domain_node = _.graph.nodes                       () [0]
            model_node  = _.graph.model.nodes                 () [0]
            schema_node = list(_.graph.model.data.nodes.values())[0]

            assert type(domain_node                                ) == Domain__Mermaid__Node
            assert type(domain_node.node                           ) == Model__Mermaid__Node
            assert type(domain_node.graph                          ) == Model__Mermaid__Graph
            assert type(domain_node.graph.data                     ) == Schema__Mermaid__Graph
            assert type(domain_node.graph.data.schema_types) == Schema__Mermaid__Types
            assert domain_node.graph.model_types. node_model_type == Model__Mermaid__Node

            assert type(model_node                 ) == Model__Mermaid__Node
            assert type(model_node.data            ) == Schema__Mermaid__Node

            assert type(schema_node                ) == Schema__Mermaid__Node
            assert type(schema_node.node_data    ) == Schema__Mermaid__Node__Data

            domain_edge = _.graph.edges                       () [0]
            model_edge  = _.graph.model.edges                 () [0]
            schema_edge = list(_.graph.model.data.edges.values())[0]

            assert type(domain_edge                               ) == Domain__Mermaid__Edge
            assert type(domain_edge.edge                          ) == Model__Mermaid__Edge
            assert type(domain_edge.graph                         ) == Model__Mermaid__Graph
            assert type(domain_edge.graph.data                    ) == Schema__Mermaid__Graph
            assert type(domain_edge.graph.data.schema_types) == Schema__Mermaid__Types
            assert domain_edge.graph.model_types.edge_model_type == Model__Mermaid__Edge

            assert type(model_edge                 ) == Model__Mermaid__Edge
            assert type(model_edge.data            ) == Schema__Mermaid__Edge

            assert type(schema_node                ) == Schema__Mermaid__Node
            assert type(schema_node.node_data    ) == Schema__Mermaid__Node__Data

            assert type(schema_edge                ) == Schema__Mermaid__Edge