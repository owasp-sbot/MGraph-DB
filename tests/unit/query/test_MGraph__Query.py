import pytest
from unittest                                                       import TestCase
from osbot_utils.testing.__                                         import __
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.providers.simple.schemas.Schema__Simple__Node        import Schema__Simple__Node
from mgraph_db.mgraph.actions.MGraph__Index                         import MGraph__Index
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.providers.simple.MGraph__Simple__Test_Data           import MGraph__Simple__Test_Data
from mgraph_db.query.MGraph__Query                                  import MGraph__Query
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.utils.Env                                          import load_dotenv
from osbot_utils.utils.Objects                                      import base_types
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id

class Test_Edge(Schema__MGraph__Edge): pass                                                 # Create test edge type

class test_MGraph__Query__Methods(TestCase):

    def setUp(self):
        self.mgraph       = MGraph__Simple__Test_Data().create()                    # Create test graph
        self.graph        = self.mgraph.graph
        self.mgraph_index = MGraph__Index.from_graph(self.graph)                    # Create index
        self.mgraph_data  = MGraph__Data(graph=self.mgraph.graph)                   # Create data access
        self.query        = MGraph__Query(mgraph_index = self.mgraph_index,         # Create query instance
                                          mgraph_data   = self.mgraph_data ).setup()

    def test_init(self):                                                       # Test initialization
        with self.query as _:
            assert type(_)              is MGraph__Query
            assert base_types(_)        == [Type_Safe, object]
            assert type(_.mgraph_index) is MGraph__Index
            assert type(_.mgraph_data)  is MGraph__Data
            assert _.obj()              == __(mgraph_data  = _.mgraph_data .obj(),
                                              mgraph_index = _.mgraph_index.obj(),
                                              query_views  = _.query_views .obj(),
                                              root_nodes   = []                 )
            initial_view    = _.current_view()                                              # test .setup() method (which will create a default view)
            initial_view_id = initial_view.view_id()
            assert _.query_views.json() == {'data': { 'current_view_id': str(initial_view_id),
                                                      'first_view_id'  : str(initial_view_id),
                                                      'views'          : { str(initial_view_id): initial_view.data.json() }}}



    def test__get_source_ids(self):                                           # Test _get_source_ids
        with self.mgraph.data() as _:
            expected_nodes = set(_.nodes_ids())
            expected_edges = set(_.edges_ids())

        nodes, edges = self.query.get_source_ids()                           # Call method

        assert type(nodes)          is set                                    # Check types
        assert type(edges)          is set
        assert nodes               == expected_nodes                          # Check values
        assert edges               == expected_edges

    def test__get_current_ids__no_view(self):                                # Test _get_current_ids with no view
        current_nodes, current_edges = self.query.get_current_ids()

        assert current_nodes == set()                                        # Should be empty
        assert current_edges == set()

    def test__get_current_ids__with_view(self):                             # Test _get_current_ids with view
        test_nodes = {Node_Id(Obj_Id()), Node_Id(Obj_Id())}
        test_edges = {Edge_Id(Obj_Id()), Edge_Id(Obj_Id())}

        self.query.create_view(                                             # Create test view
            nodes_ids = test_nodes,
            edges_ids = test_edges,
            operation = 'test',
            params    = {}
        )

        current_nodes, current_edges = self.query.get_current_ids()

        assert current_nodes == test_nodes                                   # Should return view IDs
        assert current_edges == test_edges

    def test__get_connecting_edges(self):                                    # Test _get_connecting_edges
        with self.mgraph.edit() as _:                                     # Create test nodes and edges
            node1 = _.new_node(value='test1')
            node2 = _.new_node(value='test2')
            edge  = _.new_edge(from_node_id = node1.node_id,
                                  to_node_id   = node2.node_id)
            test_nodes = {node1.node_id, node2.node_id}

        with self.query as _:
            _.re_index()
            edges = _.get_connecting_edges(test_nodes)                 # Get connecting edges

        assert type(edges) is set                                           # Check result
        assert edge.edge_id in edges
        assert len(edges) == 1

    def test__create_view__first_view(self):                                # Test _create_view with no previous view
        test_nodes = {Node_Id(Obj_Id()), Node_Id(Obj_Id())}
        test_edges = {Edge_Id(Obj_Id()), Edge_Id(Obj_Id())}
        initial_view = self.query.query_views.current_view()
        self.query.create_view(nodes_ids = test_nodes       ,               # Create first view
                               edges_ids = test_edges       ,
                               operation = 'test_op'        ,
                               params    = {'test': 'value'})

        view = self.query.query_views.current_view()                         # Check view
        assert view.nodes_ids()       == test_nodes
        assert view.edges_ids()       == test_edges
        assert view.query_operation() == 'test_op'
        assert view.query_params()    == {'test': 'value'}
        assert view.previous_view_id() == initial_view.view_id()

    def test__create_view__with_previous(self):                             # Test _create_view with previous view
        # Create first view
        self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = {Obj_Id()},
            operation = 'first',
            params    = {}
        )
        first_view = self.query.query_views.current_view()

        # Create second view
        test_nodes = {Obj_Id(), Obj_Id()}
        test_edges = {Obj_Id(), Obj_Id()}

        self.query.create_view(
            nodes_ids = test_nodes,
            edges_ids = test_edges,
            operation = 'second',
            params    = {}
        )

        second_view = self.query.query_views.current_view()
        assert second_view.previous_view_id() == first_view.view_id()
        assert first_view.next_view_ids()     == {second_view.view_id()}

    def test_by_type(self):                                                  # Test by_type method
        result = self.query.by_type(Schema__Simple__Node)                    # Query by type

        current_view = self.query.query_views.current_view()                 # Check view
        assert current_view.query_operation() == 'by_type'
        assert current_view.query_params()    == {'type': Schema__Simple__Node.__name__}

        with self.mgraph.data() as _:                                        # Check results
            assert current_view.nodes_ids() == set(_.nodes_ids())
            assert len(current_view.nodes_ids()) == 3                        # Should find all test nodes

    def test_by_type__filtered(self):                                        # Test by_type with existing filter
        # First filter
        self.query.create_view(
            nodes_ids = {self.mgraph.data().nodes()[0].node_id},            # Just one node
            edges_ids = set(),
            operation = 'filter',
            params    = {}
        )

        # Then query by type
        result = self.query.by_type(Schema__Simple__Node)

        current_view = self.query.query_views.current_view()
        assert len(current_view.nodes_ids()) == 1                            # Should maintain filter

    def test_go_back__no_history(self):                                      # Test go_back with no history
        assert self.query.go_back()                  is False                # Should return False

    def test_go_back__with_history(self):                                    # Test go_back with history
        # Create history
        view1 = self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'first',
            params    = {}
        )

        view2 = self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'second',
            params    = {}
        )

        assert self.query.go_back() is True                                  # Go back
        current = self.query.query_views.current_view()
        assert current.query_operation() == 'first'                          # Should be at first view

    def test_go_forward__no_next(self):                                      # Test go_forward with no next view
        self.query.create_view(                                             # Create single view
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'test',
            params    = {}
        )

        assert self.query.go_forward() is False                              # Should return False

    def test_go_forward__with_next(self):                                    # Test go_forward with next view
        # Create views
        self.query.create_view(nodes_ids = {Obj_Id()},
                               edges_ids = set()     ,
                               operation = 'first'  ,
                               params    = {}       )

        self.query.create_view(nodes_ids = {Obj_Id()},
                               edges_ids = set()     ,
                               operation = 'second' ,
                               params    = {}       )

        self.query.go_back()                                                 # Go back to first
        assert self.query.go_forward() is True                               # Go forward
        current = self.query.query_views.current_view()
        assert current.query_operation() == 'second'                         # Should be at second view

    def test_go_forward__specific_view(self):                                # Test go_forward with specific view ID
        # Create branching views
        self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'root',
            params    = {}
        )

        self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'branch1',
            params    = {}
        )

        self.query.go_back()                                                 # Go back to root

        branch2 = self.query.create_view(                                   # Create second branch
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'branch2',
            params    = {}
        )

        self.query.go_back()                                                 # Go back to root
        branch2_view = self.query.query_views.get_view(branch2.view_id())

        assert self.query.go_forward(branch2_view.view_id()) is True         # Go to specific branch
        current = self.query.query_views.current_view()
        assert current.query_operation() == 'branch2'                         # Should be at branch2

    def test_go_forward__invalid_view(self):                                 # Test go_forward with invalid view ID
        self.query.create_view(                                             # Create views
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'first',
            params    = {}
        )

        self.query.create_view(
            nodes_ids = {Obj_Id()},
            edges_ids = set(),
            operation = 'second',
            params    = {}
        )

        self.query.go_back()
        assert self.query.go_forward(Obj_Id()) is False                      # Should return False for invalid ID

    def test_collect(self):
        nodes = self.query.by_type(Schema__Simple__Node).collect()
        assert len(nodes) == 3
        assert all(isinstance(node, Domain__MGraph__Node) for node in nodes)

    def test_first(self):
        node = self.query.by_type(Schema__Simple__Node).first()
        assert isinstance(node, Domain__MGraph__Node)
        assert node.node_data.value in ['A', 'B', 'C']

    def test_exists(self):
        assert self.query.by_type(Schema__Simple__Node).exists()
        #assert not self.query.with_field('name', 'NonexistentNode').exists()        #todo: rethink how this .exists() is supposed to work

    @pytest.mark.skip("Needs fixing after refactoring of MGraph__Index")  # for example get_nodes_by_field() doesn't exist any more
    def test_traverse(self):
        start     = self.query.with_field('name', 'Node 1')
        connected = start.traverse()
        assert connected.count() == 1                                       # todo: double check if this is correct (or if it should be 2)

    @pytest.mark.skip("Needs fixing after refactoring of MGraph__Index")  # for example get_nodes_by_field() doesn't exist any more
    def test_traverse_with_edge_type(self):
        start     = self.query.with_field('name', 'Node 1')
        connected = start.traverse(edge_type=Domain__MGraph__Edge)
        assert connected.count() == 1                                       # todo: double check if this is correct (or if it should be 2)

    def test_filter(self):
        result = self.query.by_type(Schema__Simple__Node).filter(
            lambda node: node.node_data.value in ['A', 'B']
        )
        assert result.count() == 2
        values = [node.node_data.value for node in result.collect()]
        assert sorted(values) == ['A', 'B']

    @pytest.mark.skip("needs fixing due bug in how the edges are added to the query")       # todo: fix this
    def test_with_node_value(self):
        mgraph = MGraph()
        with mgraph.edit() as _:                                                              # Create test data
            #pprint(_.new_node(node_type=Schema__MGraph__Node__Value, value="test1", value_type=str))
            node_1 = _.new_node(node_type=Schema__MGraph__Node__Value, value="test1", value_type=str)
            node_2 = _.new_node(node_type=Schema__MGraph__Node__Value, value="test2", value_type=str)
            node_3 = _.new_node(node_type=Schema__MGraph__Node__Value, value="42"   , value_type=int)
            node_4 = _.new_node(node_type=Schema__MGraph__Node__Value, value="12"   , value_type=int)

            # Create connections using different edge types
            edge_1 = _.new_edge(from_node_id = node_1.node_id, to_node_id = node_2.node_id, edge_type = Test_Edge            )
            edge_2 = _.new_edge(from_node_id = node_2.node_id,to_node_id  = node_3.node_id, edge_type = Schema__MGraph__Edge)
            edge_3 = _.new_edge(from_node_id = node_2.node_id,to_node_id  = node_4.node_id, edge_type = Schema__MGraph__Edge)

        load_dotenv()

        with mgraph.query() as _:
            #_.re_index()                                                                            # Rebuild index with new data

            # Test without edge type filter
            result = _.with_node_value(42)
            #pprint(type(result))
            result.save_to_png('./test_MGraph__Query.exported.png', show_source_graph=True, show_node__value=True)


            assert result.count() == 1
            first_node = result.first()
            assert first_node.node_data.value == "test1"

            # Test with edge type filter
            result = _.with_node_value("test2", Test_Edge)
            assert result.count() == 1
            first_node = result.first()
            assert first_node.node_data.value == "test2"

            # Test with different value type (int)
            result = _.with_node_value(42)
            assert result.count() == 1
            first_node = result.first()
            assert first_node.node_data.value == "42"                                              # Note: stored as string

            # Test non-existent value
            result = _.with_node_value("non_existent")
            assert result.count() == 0

            # Test query operation and params
            current_view = result.current_view()
            assert current_view.query_operation() == 'with_value'
            assert current_view.query_params()['value_type'] == str.__name__
            assert current_view.query_params()['value'] == "non_existent"