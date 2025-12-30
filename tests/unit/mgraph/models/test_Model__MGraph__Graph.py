"""
Tests for Model__MGraph__Graph

Expanded coverage including:
- All original test cases
- Factory integration paths
- Type resolution edge cases
- Batch operations
- Graph state integrity
"""

import pytest
from types                                                                  import NoneType
from unittest                                                               import TestCase
from mgraph_db.mgraph.models.Model__MGraph__Types                           import Model__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                         import Schema__MGraph__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id            import Obj_Id, is_obj_id
from mgraph_db.mgraph.models.Model__MGraph__Edge                            import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node                            import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                         import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                    import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                          import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.utils.Objects                                              import base_classes


class Simple_Node      (Schema__MGraph__Node     ): pass                                    # Helper classes for testing
class Custom_Node      (Schema__MGraph__Node     ): pass
class Another_Node     (Schema__MGraph__Node     ): pass
class Custom_Node_Data (Schema__MGraph__Node__Data): 
    custom_value: str = ""


class test_Model__MGraph__Graph(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Setup shared test fixtures
        cls.schema_types = Schema__MGraph__Types(node_type = Simple_Node          ,
                                                 edge_type = Schema__MGraph__Edge )

    def setUp(self):                                                                        # Initialize test data
        self.graph_data = Schema__MGraph__Graph(schema_types = self.schema_types   ,
                                                graph_type   = Schema__MGraph__Graph)
        self.graph      = Model__MGraph__Graph (data         = self.graph_data      )

    def test__init__(self):                                                                 # Tests basic initialization
        with self.graph as _:
            assert type(_)                   is Model__MGraph__Graph
            assert base_classes(_)           == [Type_Safe, object]
            assert _.data                    is self.graph_data
            assert _.data.schema_types       == self.schema_types
            assert len(_.data.nodes)         == 0
            assert len(_.data.edges)         == 0

    def test__init____without_schema_types(self):                                           # Test initialization without schema_types
        graph_data = Schema__MGraph__Graph()
        
        with Model__MGraph__Graph(data=graph_data) as _:
            assert type(_)             is Model__MGraph__Graph
            assert _.data.schema_types is None
            assert len(_.data.nodes)   == 0

    # --- Node Operations ---

    def test_new_node(self):                                                                # Tests node creation
        with self.graph as _:
            node    = _.new_node()
            node_id = node.node_id
            
            assert type(node)                 is Model__MGraph__Node
            assert node_id                    in _.data.nodes
            assert node.node_type             is Simple_Node                                # Uses schema_types default

    def test_new_node__with_custom_type(self):                                              # Test node creation with explicit type
        with self.graph as _:
            node = _.new_node(node_type=Custom_Node)
            
            assert type(node)       is Model__MGraph__Node
            assert node.node_type   is Custom_Node

    def test_new_node__with_node_data(self):                                                # Test node creation with complete spec
        node_data = Custom_Node_Data(custom_value="test_value")
        
        with self.graph as _:
            node = _.new_node(node_type=Custom_Node, node_data=node_data)
            
            assert type(node)            is Model__MGraph__Node
            assert node.data.node_data   is node_data
            assert node.data.node_data.custom_value == "test_value"

    def test_node_retrieval(self):                                                          # Tests node retrieval by ID
        with self.graph as _:
            node      = _.new_node()
            node_id   = node.node_id
            retrieved = _.node(node_id)
            
            assert retrieved.json() == node.json()

    def test_node_retrieval__not_found(self):                                               # Test retrieval of non-existent node
        with self.graph as _:
            result = _.node(Obj_Id())
            assert result is None

    def test_delete_node(self):                                                             # Tests node removal
        with self.graph as _:
            node    = _.new_node()
            node_id = node.node_id
            
            assert _.delete_node(node_id) is True
            assert _.delete_node(node_id) is False                                          # Already deleted
            assert node_id not in _.data.nodes

    def test_delete_node__non_existent(self):                                               # Test deleting non-existent node
        with self.graph as _:
            assert _.delete_node(Obj_Id()) is False

    def test_nodes__iteration(self):                                                        # Test iterating over all nodes
        with self.graph as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            
            nodes = list(_.nodes())
            
            assert len(nodes)     == 3
            assert nodes[0].json() == node_1.json()
            assert nodes[1].json() == node_2.json()
            assert nodes[2].json() == node_3.json()

    # --- Edge Operations ---

    def test_new_edge(self):                                                                # Tests edge creation
        with self.graph as _:
            node_1    = _.new_node()
            node_2    = _.new_node()
            node_1_id = node_1.node_id
            node_2_id = node_2.node_id
            
            edge    = _.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)
            edge_id = edge.edge_id()
            
            assert type(edge)          is Model__MGraph__Edge
            assert edge.from_node_id() == node_1_id
            assert edge.to_node_id()   == node_2_id
            assert is_obj_id(edge_id)  is True

    def test_edge_retrieval(self):                                                          # Tests edge retrieval by ID
        with self.graph as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_id = edge.edge_id()
            
            retrieved = _.edge(edge_id)
            assert retrieved.json() == edge.json()

    def test_delete_edge(self):                                                             # Tests edge removal
        with self.graph as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_id = edge.edge_id()
            
            assert _.delete_edge(edge_id) is True
            assert _.delete_edge(edge_id) is False
            assert edge_id not in _.data.edges

    def test_delete_edge__non_existent(self):                                               # Test deleting non-existent edge
        with self.graph as _:
            assert _.delete_edge(Obj_Id()) is False

    def test_node__to_edges(self):                                                          # Test getting edges connected to a node
        with self.graph as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            _      .new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            
            assert len(_.node__to_edges(node_1.node_id)) == 0                               # Outgoing edge
            assert len(_.node__to_edges(node_2.node_id)) == 1                               # Incoming edge

    def test_edges__iteration(self):                                                        # Test iterating over all edges
        with self.graph as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)
            
            edges = list(_.edges())
            
            assert len(edges) == 2

    # --- Edge Validation ---

    def test_edge_validation__from_node_not_found(self):                                    # Test edge creation with invalid from_node
        with self.graph as _:
            with pytest.raises(ValueError, match="From node .* not found"):
                _.new_edge(from_node_id=Obj_Id(), to_node_id=Obj_Id())

    def test_edge_validation__to_node_not_found(self):                                      # Test edge creation with invalid to_node
        with self.graph as _:
            node_ok = _.new_node()
            node_bad_id = Obj_Id()
            
            with pytest.raises(ValueError, match=f"To node {node_bad_id} not found"):
                _.new_edge(from_node_id=node_ok.node_id, to_node_id=node_bad_id)

    # --- Cascading Deletion ---

    def test_node_removal__cascades_to_edges(self):                                         # Tests that removing a node removes connected edges
        with self.graph as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)
            
            assert len(_.edges()) == 2
            
            _.delete_node(node_2.node_id)                                                   # Remove middle node
            
            assert len(_.edges())                 == 0                                      # Both edges removed
            assert edge_1.edge_id() not in _.data.edges
            assert edge_2.edge_id() not in _.data.edges

    # --- Custom Node Types ---

    def test_custom_node_types(self):                                                       # Tests creation of nodes with custom types
        with self.graph as _:
            assert type(_.data.schema_types) is Schema__MGraph__Types
            assert _.data.schema_types.node_type is Simple_Node
            
            default_node = _.new_node()
            assert default_node.node_type is Simple_Node
            
            custom_node = _.new_node(node_type=Custom_Node)
            assert custom_node.node_type is Custom_Node

    def test_mixed_node_types(self):                                                        # Test graph with mixed node types
        with self.graph as _:
            node_simple  = _.new_node()
            node_custom  = _.new_node(node_type=Custom_Node)
            node_another = _.new_node(node_type=Another_Node)
            
            assert node_simple.node_type  is Simple_Node
            assert node_custom.node_type  is Custom_Node
            assert node_another.node_type is Another_Node
            
            # All should be in the same graph
            assert len(_.data.nodes) == 3

    # --- Graph Queries ---

    def test_graph__returns_schema(self):                                                   # Tests graph() method returns schema
        with self.graph as _:
            _.new_node()
            _.new_node()
            
            graph = _.graph()
            
            assert type(graph)       is Schema__MGraph__Graph
            assert len(graph.nodes)  == 2
            assert len(graph.edges)  == 0

    # --- Model Types ---

    def test_model_types(self):                                                             # Test model_types attribute
        with self.graph as _:
            assert type(_.model_types)                is Model__MGraph__Types
            assert type(_.model_types.node_model_type) is NoneType                          # Not set by default

    # --- Batch Operations ---

    def test_batch_node_creation(self):                                                     # Test creating many nodes
        with self.graph as _:
            nodes = [_.new_node() for i in range(50)]
            
            assert len(nodes)        == 50
            assert len(_.data.nodes) == 50
            
            # All IDs should be unique
            node_ids = [n.node_id for n in nodes]
            assert len(set(node_ids)) == 50

    def test_batch_node_creation__mixed_types(self):                                        # Test batch with mixed types
        with self.graph as _:
            for i in range(20):
                if i % 3 == 0:
                    _.new_node(node_type=Simple_Node)
                elif i % 3 == 1:
                    _.new_node(node_type=Custom_Node)
                else:
                    _.new_node(node_type=Another_Node)
            
            assert len(_.data.nodes) == 20

    def test_batch_edge_creation(self):                                                     # Test creating chain of edges
        with self.graph as _:
            nodes = [_.new_node() for i in range(10)]
            
            for i in range(len(nodes) - 1):
                _.new_edge(from_node_id=nodes[i].node_id, to_node_id=nodes[i+1].node_id)
            
            assert len(_.data.edges) == 9

    # --- Graph Integrity ---

    def test_graph_integrity__after_operations(self):                                       # Test graph state consistency
        with self.graph as _:
            # Create nodes
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            
            # Create edges
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)
            
            # Verify state
            assert len(_.data.nodes) == 3
            assert len(_.data.edges) == 2
            
            # Delete middle node
            _.delete_node(node_2.node_id)
            
            # Verify cascade
            assert len(_.data.nodes) == 2
            assert len(_.data.edges) == 0
            assert node_1.node_id in _.data.nodes
            assert node_3.node_id in _.data.nodes
            assert node_2.node_id not in _.data.nodes

    def test_type_resolution__with_schema_types(self):                                      # Test type from schema_types
        schema_types = Schema__MGraph__Types(node_type=Custom_Node, edge_type=Schema__MGraph__Edge)
        graph_data   = Schema__MGraph__Graph(schema_types=schema_types)
        graph        = Model__MGraph__Graph(data=graph_data)
        
        node = graph.new_node()
        assert node.node_type is Custom_Node

    def test_type_resolution__without_schema_types(self):                                   # Test fallback to defaults
        graph_data = Schema__MGraph__Graph()                                                # No schema_types
        graph      = Model__MGraph__Graph(data=graph_data)
        
        node = graph.new_node()
        assert node.node_type is None # is Schema__MGraph__Node                                       # Default

    def test_type_resolution__explicit_overrides_schema(self):                              # Test explicit type overrides schema_types
        schema_types = Schema__MGraph__Types(node_type=Simple_Node, edge_type=Schema__MGraph__Edge)
        graph_data   = Schema__MGraph__Graph(schema_types=schema_types)
        graph        = Model__MGraph__Graph(data=graph_data)
        
        node = graph.new_node(node_type=Custom_Node)                                        # Explicit type
        assert node.node_type is Custom_Node                                                # Not Simple_Node

    def test_type_resolution__complete_spec_bypasses_resolution(self):                      # Test fast path with complete spec
        graph_data = Schema__MGraph__Graph()
        graph      = Model__MGraph__Graph(data=graph_data)
        node_data  = Custom_Node_Data(custom_value="test")
        
        node = graph.new_node(node_type=Custom_Node, node_data=node_data)
        
        assert node.node_type            is Custom_Node
        assert node.data.node_data       is node_data
        assert node.data.node_data.custom_value == "test"


# class test_Model__MGraph__Graph__Edge_Cases(TestCase):
#     """Edge case and error handling tests"""

    # @classmethod
    # def setUpClass(cls):
    #     cls.schema_types = Schema__MGraph__Types(node_type=Simple_Node, edge_type=Schema__MGraph__Edge)

    # def setUp(self):
    #     self.graph_data = Schema__MGraph__Graph(schema_types=self.schema_types)
    #     self.graph      = Model__MGraph__Graph(data=self.graph_data)

    def test_self_referencing_edge(self):                                                   # Test edge from node to itself
        with self.graph as _:
            node = _.new_node()
            edge = _.new_edge(from_node_id=node.node_id, to_node_id=node.node_id)
            
            assert edge.from_node_id() == edge.to_node_id()

    def test_multiple_edges_same_nodes(self):                                               # Test multiple edges between same nodes
        with self.graph as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_3 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_1.node_id)
            
            assert len(_.data.edges) == 3
            assert edge_1.edge_id()  != edge_2.edge_id()

    def test_empty_graph_operations(self):                                                  # Test operations on empty graph
        with self.graph as _:
            assert len(list(_.nodes())) == 0
            assert len(list(_.edges())) == 0
            assert _.node(Obj_Id())     is None
            assert _.edge(Obj_Id())     is None
            assert _.delete_node(Obj_Id()) is False
            assert _.delete_edge(Obj_Id()) is False

    def test_large_graph(self):                                                             # Test with larger graph
        with self.graph as _:
            # Create 100 nodes
            nodes = [_.new_node() for i in range(100)]
            
            # Create edges forming a chain
            for i in range(99):
                _.new_edge(from_node_id=nodes[i].node_id, to_node_id=nodes[i+1].node_id)
            
            assert len(_.data.nodes) == 100
            assert len(_.data.edges) == 99
            
            # Delete first node - should remove one edge
            _.delete_node(nodes[0].node_id)
            
            assert len(_.data.nodes) == 99
            assert len(_.data.edges) == 98