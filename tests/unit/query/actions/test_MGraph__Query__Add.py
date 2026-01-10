import pytest
import re
from unittest                                                                   import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Node                               import Domain__MGraph__Node
from mgraph_db.mgraph.MGraph                                                    import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                              import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph                               import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value                       import Schema__MGraph__Node__Value
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges import Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Hour, Schema__MGraph__Time_Series__Edge__Month
from mgraph_db.query.actions.MGraph__Query__Add                                 import MGraph__Query__Add
from mgraph_db.query.domain.Domain__MGraph__Query                               import Domain__MGraph__Query


class test_MGraph__Query__Add(TestCase):

    def setUp(self):
        self.model_graph  = Model__MGraph__Graph ()
        self.graph        = Domain__MGraph__Graph(model = self.model_graph)
        self.mgraph       = MGraph               (graph = self.graph      )
        self.query        = Domain__MGraph__Query(mgraph_data  = self.mgraph.data() ,
                                                  mgraph_index = self.mgraph.index(), )
        self.query.setup()
        self.add_action   = MGraph__Query__Add   (query = self.query)

    # def tearDown(self):
    #     load_dotenv()
    #     mgraph_query = MGraph__Query()
    #     mgraph_query.query_views  = self.query.query_views
    #     mgraph_query.mgraph_index = self.query.mgraph_index
    #     mgraph_query.mgraph_data  = self.query.mgraph_data
    #
    #     with MGraph__Query__Screenshot(mgraph_query=mgraph_query) as _:
    #         #_.show_source_graph = True
    #         #_.show_node__value  = True
    #         #_.show_node__type  = True
    #         _.show_edge__type  = True
    #         _.save_to('./test_MGraph__Query__Add.both.png')

        # with self.mgraph.screenshot() as _:
        #     _.load_dotenv   ()
        #     _.show_edge__id()
        #     _.save_to('test_MGraph__Query__Filter.png').dot()


    def test_setup(self):
        with self.add_action as _:
            assert type(_) is MGraph__Query__Add
            assert _.query == self.query

    def test_add_node_id(self):                                                     # Test adding single node
        add_action                   = self.add_action
        node                         = self.mgraph.edit().new_node()                                  # Create test node
        result                       = add_action.add_node_id(node.node_id)                           # Add node to view
        current_nodes, current_edges = self.query.get_current_ids()

        assert type(result)     is MGraph__Query__Add
        assert result           == add_action                                                 # Verify result,  Should return self for chaining
        assert current_nodes    == {node.node_id}
        assert current_edges    == set()  # No edges added

        #error_message = "Parameter 'node_id' expected type <class 'osbot_utils.type_safe.primitives.domains.identifiers.Node_Id.Node_Id'>, but got <class 'str'>"
        error_message = "in Node_Id: value provided was not a valid Node_Id: invalid_id"    # with @type_safe disabled, this is the error we now get
        with pytest.raises(ValueError, match=re.escape(error_message)):
            add_action.add_node_id('invalid_id')                                            # Test adding non-existent node
        current_nodes, current_edges = self.query.get_current_ids()


        assert current_nodes    == {node.node_id}                                     # No change to nodes
        assert current_edges    == set()

    def test_add_nodes_ids(self):                                               # Test adding multiple nodes
        add_action = self.add_action

        # Create test nodes
        node_1 = self.graph.new_node()
        node_2 = self.graph.new_node()
        node_3 = self.graph.new_node()

        # Add multiple nodes
        result = add_action.add_nodes_ids({node_1.node_id, node_2.node_id})

        # Verify initial add
        assert result == add_action
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id}
        assert current_edges == set()

        # Add another node
        add_action.add_nodes_ids({node_3.node_id})
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

        # Test adding mix of valid and invalid nodes
        #error_message = "Parameter 'node_id' expected type <class 'osbot_utils.type_safe.primitives.domains.identifiers.Node_Id.Node_Id'>, but got <class 'str'>"
        error_message = "in Node_Id: value provided was not a valid Node_Id: invalid_id" # with @type_safe disabled this is the message we get
        with pytest.raises(ValueError, match=re.escape(error_message)):
            add_action.add_nodes_ids({node_1.node_id, 'invalid_id'})

        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

        # Test adding only invalid nodes
        #error_message = "Parameter 'node_id' expected type <class 'osbot_utils.type_safe.primitives.domains.identifiers.Node_Id.Node_Id'>, but got <class 'str'>"
        error_message = "in Node_Id: value provided was not a valid Node_Id: invalid_1" # with @type_safe disabled this is the message we get
        with pytest.raises(ValueError, match=re.escape(error_message)):
            #add_action.add_nodes_ids({'invalid_1', 'invalid_2'})           # this is a set
            add_action.add_nodes_ids({'invalid_1'})                         # so we need to only have one value to make the error deterministic

        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

    def test_add_node_with_value(self):                                                                 # Test adding node by value
        add_action = self.add_action

        new_node_kwargs =  dict(node_type  = Schema__MGraph__Node__Value,
                                value      = "test_value",
                                value_type = str)
        value_node      = self.graph.new_node(**new_node_kwargs)    # Create value node

        self.query.mgraph_index.values_index.add_value_node(value_node)                                 # Add value to index


        result = add_action.add_node_with_value("test_value")                                           # Test adding by value

        assert type(value_node) is Domain__MGraph__Node
        assert result           == add_action                                                                     # Verify result
        current_nodes, _ = self.query.get_current_ids()

        assert value_node.node_id in current_nodes

        add_action.add_node_with_value("non_existent_value")                                            # Test adding non-existent value
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {value_node.node_id}                                                    # No change to nodes

    def test_add_outgoing_edges(self):                                          # Test adding outgoing edges
        add_action = self.add_action


        with self.mgraph.edit() as _:                                           # Create test nodes and edges
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()

            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)


        result_1                     = add_action.add_node_id(node_1.node_id)               # Start with node_1
        result_2                     = add_action.add_outgoing_edges(depth=1)               # Add outgoing edges with depth=1
        current_nodes, current_edges = self.query.get_current_ids()

        assert result_1      == result_2
        assert result_2      == add_action                                                  # Verify first level
        assert current_nodes == {node_1.node_id, node_2.node_id}
        assert current_edges == {edge_1.edge_id}


        add_action.add_outgoing_edges(depth=2)                                              # Add outgoing edges with depth=2
        current_nodes, current_edges = self.query.get_current_ids()

        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}

        add_action.add_outgoing_edges(depth=0)                                              # Test with invalid depth
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}                            # no changes in current_nodes


        add_action.add_outgoing_edges()                                                     # Test with None depth (should have no impact too)
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}


    def test_add_operations_chaining(self):                                                     # Test method chaining
        with self.mgraph.edit() as _:                                                           # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            edge   = _.connect_nodes(node_1, node_2)

        with self.add_action as _:                                                              # Test chaining multiple operations
            result = (_.add_node_id       (node_1.node_id)
                       .add_nodes_ids     ({node_2.node_id, node_3.node_id})
                       .add_outgoing_edges())

        current_nodes, current_edges = self.query.get_current_ids()                             # Verify final state
        assert result        == self.add_action
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge.edge_id}

    def test_add_nodes_with_edge_no_matches(self):                                              # Test edge cases with no matches
        with self.mgraph.edit() as _:                                                           # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()

            _.new_edge(from_node_id = node_1.node_id                        ,
                       to_node_id   = node_2.node_id                        ,
                       edge_type    = Schema__MGraph__Time_Series__Edge__Day)


        result_1 = (self.add_action.add_node_id      (node_1.node_id)                           # Test with no matching edge type
                        .add_nodes_with_outgoing_edge(Schema__MGraph__Time_Series__Edge__Year))

        current_nodes_1, current_edges_1 = self.query.get_current_ids()

        assert result_1         == self.add_action
        assert current_nodes_1  == {node_1.node_id}  # No new nodes added
        assert current_edges_1  == set()  # No edges added

    def test_add_nodes_with_edge_matche_but_no_nodes(self):                             # Test with matching edge type but no matching nodes in current view
        with self.mgraph.edit() as _:                                                           # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()

            _.new_edge(from_node_id=node_1.node_id,
                       to_node_id=node_2.node_id,
                       edge_type=Schema__MGraph__Time_Series__Edge__Day)

        result_2 = (self.add_action.add_node_id(node_2.node_id)                         # Start with target node
                    .add_nodes_with_outgoing_edge(
            Schema__MGraph__Time_Series__Edge__Day))  # Look for outgoing Day edges

        current_nodes_2, current_edges_2 = self.query.get_current_ids()

        assert result_2 == self.add_action
        assert current_nodes_2 == {node_2.node_id}  # No new nodes added
        assert current_edges_2 == set()  # No edges added

    def test_add_nodes_with_incoming_edge(self):                                                    # Test adding nodes with specific incoming edges
        with self.mgraph.edit() as _:                                                                   # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()

            _.new_edge(from_node_id=node_1.node_id,
                      to_node_id  =node_2.node_id,
                      edge_type   =Schema__MGraph__Time_Series__Edge__Year)

            _.new_edge(from_node_id=node_3.node_id,
                      to_node_id  =node_2.node_id,
                      edge_type   =Schema__MGraph__Time_Series__Edge__Year)

            _.new_edge(from_node_id=node_1.node_id,
                      to_node_id  =node_3.node_id,
                      edge_type   =Schema__MGraph__Time_Series__Edge__Month)       # Different edge type

        result = (self.add_action.add_node_id(node_2.node_id)                                          # Start with target node
                                 .add_nodes_with_incoming_edge(Schema__MGraph__Time_Series__Edge__Year))# Add nodes with incoming Year edges

        current_nodes, current_edges = self.query.get_current_ids()

        assert result         == self.add_action                                                        # Verify method chaining
        assert current_nodes  == {node_1.node_id, node_2.node_id, node_3.node_id}                     # Both source nodes added
        assert current_edges  == set()                                                                  # No edges should be added

    def test_add_nodes_with_outgoing_edge(self):                                                      # Test adding nodes with specific outgoing edges
        with self.mgraph.edit() as _:                                                                   # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()

            edge_1 = _.new_edge(from_node_id= node_1.node_id,
                                to_node_id  = node_2.node_id,
                                edge_type   = Schema__MGraph__Time_Series__Edge__Day)

            edge_2 = _.new_edge(from_node_id = node_1.node_id,
                                to_node_id   = node_3.node_id,
                                edge_type    = Schema__MGraph__Time_Series__Edge__Day)

            edge_3 = _.new_edge(from_node_id = node_2.node_id,
                                to_node_id   = node_3.node_id,
                                edge_type    = Schema__MGraph__Time_Series__Edge__Hour)       # Different edge type
        connect_edges = True
        edge_type     = Schema__MGraph__Time_Series__Edge__Day
        result        = (self.add_action.add_node_id(node_1.node_id)                                    # Start with source node
                                        .add_nodes_with_outgoing_edge(edge_type, connect_edges))        # Add nodes with outgoing Day edges and connect to existing nodes (in view)

        current_nodes, current_edges = self.query.get_current_ids()

        assert result         == self.add_action                                                        # Verify method chaining
        assert current_nodes  == {node_1.node_id, node_2.node_id, node_3.node_id}                       # Both target nodes added
        assert current_edges  == {edge_1.edge_id, edge_2.edge_id                }                       # only the day edges should had been added


    def test_view_state_management(self):                                               # Test view state after operations
        with self.mgraph.edit() as _:                                                   # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        initial_view = self.query.current_view()

        self.add_action.add_node_id(node_1.node_id)                                     # Add first node
        first_view = self.query.current_view()
        with first_view.data.view_data as _:
            assert _.query_operation == 'add_node_id'                                   # Verify operation metadata
            assert _.query_params    == {'node_id': str(node_1.node_id)}
        self.add_action.add_outgoing_edges()                                            # Add edges

        second_view = self.query.current_view()

        assert second_view.data.view_data.query_operation == 'add_outgoing_edges'      # Verify operation metadata
        assert initial_view                               != first_view                # Verify view changed
        assert first_view                                 != second_view

    def test_new_view(self):                                                          # Test new view creation
        with self.mgraph.edit() as _:                                                  # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        result = self.add_action.new_view(additional_nodes = {node_1.node_id}        ,
                                          operation        = 'test_operation'         ,
                                          params           = {'test_param': 'value'})

        current_nodes, current_edges = self.query.get_current_ids()
        current_view = self.query.current_view()

        assert result                                      == self.add_action               # Verify method chaining
        assert current_nodes                               == {node_1.node_id}              # Verify nodes added
        assert current_view.data.view_data.query_operation == 'test_operation'              # Verify operation metadata
        assert current_view.data.view_data.query_params    == {'test_param': 'value'}

    def test_combined_add_operations(self):                                           # Test combining different add operations
        with self.mgraph.edit() as _:                                                  # Create test data
            new_node_kwargs = dict(node_type  = Schema__MGraph__Node__Value,
                                   value      = "test_value"               ,
                                   value_type = str                        )

            value_node = _.new_node(**new_node_kwargs)

            node_2 = _.new_node()
            edge = _.new_edge(from_node_id=value_node.node_id, to_node_id=node_2.node_id)

        result = (self.add_action.add_node_with_value("test_value")                   # Combine different add operations
                                 .add_nodes_ids({node_2.node_id})
                                 .add_outgoing_edges())

        current_nodes, current_edges = self.query.get_current_ids()

        assert result == self.add_action                                               # Verify method chaining
        assert len(current_nodes) == 2                                                 # Verify all nodes added
        assert current_edges == {edge.edge_id}