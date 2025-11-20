from unittest                                               import TestCase
from osbot_utils.testing.__                                 import __
from mgraph_db.mgraph.MGraph                                import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_db.query.domain.Domain__MGraph__Query           import Domain__MGraph__Query
from mgraph_db.query.schemas.Schema__MGraph__Query__Views   import Schema__MGraph__Query__Views


class Simple_Node(Schema__MGraph__Node): pass                                    # Helper class for testing

class test_Domain__MGraph__Query(TestCase):

    def setUp(self):
        self.schema_graph = Schema__MGraph__Graph()
        self.model_graph  = Model__MGraph__Graph        (data=self.schema_graph)
        self.graph        = Domain__MGraph__Graph       (model=self.model_graph)
        self.mgraph       = MGraph(graph=self.graph)
        self.query        = Domain__MGraph__Query(mgraph_data=self.mgraph.data(), mgraph_index=self.mgraph.index())
        self.query.setup()

    # def tearDown(self):
    #
    #     with self.mgraph.screenshot() as _:
    #         _.load_dotenv   ()
    #         _.show_edge__id()
    #         _.save_to('test_Domain__MGraph__Query.png').dot()

    def test_setup(self):
        with self.query.query_views.data as _:
            assert type(_) is Schema__MGraph__Query__Views
            view_id = _.first_view_id
            view = _.views[view_id]
        with self.query as _:
            assert type(_) is Domain__MGraph__Query
            assert _.current_view().obj()== __(data      = __(view_id  = view_id,
                                                             view_data = __(edges_ids      = []       ,
                                                                          next_view_ids    = []       ,
                                                                          nodes_ids        = []       ,
                                                                          previous_view_id = None     ,
                                                                          query_operation  = 'initial',
                                                                          query_params     = __()     ,
                                                                          timestamp        = view.view_data.timestamp)))


    def test_create_initial_view(self):                                         # Test initial view creation
        query        = self.query
        current_view = query.current_view()

        assert current_view                    is not None
        assert current_view.query_operation()  == 'initial'
        assert len(current_view.nodes_ids  ()) == 0
        assert len(current_view.edges_ids  ()) == 0
        assert current_view.query_params   ()  == {}

    def test_get_current_ids(self):                                             # Test getting current IDs
        query = self.query

        nodes, edges = query.get_current_ids()                                  # Test with empty view
        assert nodes == set()
        assert edges == set()

        node_1 = self.graph.new_node()                                          # Add some nodes and test again
        node_2 = self.graph.new_node()
        edge   = self.graph.connect_nodes(node_1, node_2)

        query.create_view(nodes_ids = {node_1.node_id, node_2.node_id},
                          edges_ids = {edge.edge_id}                  ,
                          operation = 'test'                          ,
                          params    = {}                              )

        nodes, edges = query.get_current_ids()
        assert nodes == { node_1.node_id, node_2.node_id }
        assert edges == { edge.edge_id                   }

    def test_get_connecting_edges(self):                                       # Test edge connection detection
        query = self.query

        with self.mgraph.edit() as _:                                          # Create test nodes and edges
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            node_4 = _.new_node()

            edge_1 = _.connect_nodes(node_1, node_2)
            edge_2 = _.connect_nodes(node_2, node_3)
            edge_3 = _.connect_nodes(node_1, node_3)
            edge_4 = _.connect_nodes(node_3, node_4)

        assert self.mgraph.index() == self.query.mgraph_index

        edges_1 = query.get_connecting_edges({node_2.node_id                })  # Test with single node
        edges_2 = query.get_connecting_edges({node_1.node_id, node_2.node_id})  # Test with multiple nodes
        edges_3 = query.get_connecting_edges({node_3.node_id                })
        assert edges_1 == { edge_1.edge_id, edge_2.edge_id                  }
        assert edges_2 == { edge_1.edge_id, edge_2.edge_id, edge_3.edge_id  }
        assert edges_3 == { edge_2.edge_id, edge_3.edge_id, edge_4.edge_id  }

    def test_create_view(self):                                                     # Test view creation
        query     = self.query
        node      = self.graph.new_node()                                          # Create test data
        nodes_ids = { node.node_id }
        edges_ids = set()
        operation = "test_operation"
        params    = {"test_param": "value"}

        query.create_view(nodes_ids = nodes_ids ,
                          edges_ids = edges_ids ,
                          operation = operation ,
                          params    = params    )                                   # Create view


        current_view = query.current_view()                                         # Verify view
        assert current_view                is not None
        assert current_view.nodes_ids      () == nodes_ids
        assert current_view.edges_ids      () == edges_ids
        assert current_view.query_operation() == operation
        assert current_view.query_params   () == params

    def test_in_initial_view(self):                                         # Test initial view detection
        query = self.query
        assert query.in_initial_view() is True                              # Test right after setup

        node = self.graph.new_node()
        query.create_view(nodes_ids = {node.node_id},                       # Create a new view (which will change the current_view)
                          edges_ids = set()         ,
                          operation = 'test'        ,
                          params    = {}            )

        assert query.in_initial_view() is False

        query.create_view(nodes_ids = set(),                                # Simulate an initial view
                          edges_ids = set(),
                          operation = 'initial',
                          params    = {})

        assert query.in_initial_view() is True