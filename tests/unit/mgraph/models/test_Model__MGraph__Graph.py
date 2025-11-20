import pytest
from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Types                 import Schema__MGraph__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id, is_obj_id
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge

class Simple_Node(Schema__MGraph__Node): pass                                               # Helper class for testing

class test_Model__MGraph__Graph(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.schema_types  = Schema__MGraph__Types (node_type     = Simple_Node,
                                                    edge_type     = Schema__MGraph__Edge)
        self.graph_data    = Schema__MGraph__Graph          (schema_types  = self.schema_types     ,
                                                             graph_type    = Schema__MGraph__Graph  )
        self.graph         = Model__MGraph__Graph           (data          = self.graph_data        )

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.graph)              is Model__MGraph__Graph
        assert self.graph.data               is self.graph_data
        assert self.graph.data.schema_types == self.schema_types
        assert len(self.graph.data.nodes)    == 0
        assert len(self.graph.data.edges)    == 0

    def test_node_operations(self):                                                         # Tests node creation, addition, and removal
        node    = self.graph.new_node()                                         # Test node creation
        node_id = node.node_id
        assert isinstance(node, Model__MGraph__Node) is True
        assert node_id                                in self.graph.data.nodes

        retrieved = self.graph.node(node_id)                                                # Test node retrieval
        assert retrieved.json()                       == node.json()
        assert self.graph.delete_node(node_id)        is True                               # Test node removal
        assert self.graph.delete_node(node_id)        is False
        assert node_id                            not in self.graph.data.nodes

        assert self.graph.delete_node(Obj_Id())       is False                               # Test removing non-existent node

    def test_edge_operations(self):                                                         # Tests edge creation, addition, and removal
        node_1    = self.graph.new_node()                                            # Create two nodes
        node_2    = self.graph.new_node()
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge      = self.graph.new_edge(from_node_id=node_1_id,to_node_id=node_2_id)                                # Test edge creation
        edge_id   = edge.edge_id()
        retrieved = self.graph.edge(edge_id)                                                # Test edge retrieval

        assert isinstance(edge, Model__MGraph__Edge)     is True
        assert edge.from_node_id()                       == node_1_id
        assert edge.to_node_id  ()                       == node_2_id
        assert is_obj_id(edge_id)                        is True
        assert retrieved.json()                          == edge.json()
        assert len(self.graph.node__to_edges(node_1_id)) == 0
        assert len(self.graph.node__to_edges(node_2_id)) == 1
        assert self.graph.delete_edge(edge_id)           is True                                 # Test edge removal
        assert self.graph.delete_edge(edge_id)           is False
        assert edge_id                               not in self.graph.data.edges
        assert len(self.graph.node__to_edges(node_2_id)) == 0
        assert self.graph.delete_edge(Obj_Id())          is False                               # Test removing non-existent edge

    def test_node_removal_cascades_to_edges(self):                                          # Tests that removing a node removes connected edges
        node_1    = self.graph.new_node()
        node_2    = self.graph.new_node()
        node_3    = self.graph.new_node()
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        node_3_id = node_3.node_id

        edge_1    = self.graph.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)                               # Create edges
        edge_2    = self.graph.new_edge(from_node_id=node_2_id, to_node_id=node_3_id)
        edge_1_id = edge_1.edge_id()
        edge_2_id = edge_2.edge_id()

        assert node_1_id                         != node_2_id
        assert node_1_id                         != node_3_id
        assert edge_1_id                         != edge_2_id
        assert len(self.graph.edges())           == 2                                       # Verify initial state
        assert self.graph.delete_node(node_2_id) is True                                    # Remove node_2 (should remove both edges)
        assert len(self.graph.edges())           == 0                                       # Verify edges were removed

        assert edge_1_id not in self.graph.data.edges
        assert edge_2_id not in self.graph.data.edges

    def test_edge_validation(self):                                                         # Tests edge validation
        with pytest.raises(ValueError, match="From node .* not found"):                     # Test creating edge with non-existent nodes
            self.graph.new_edge(from_node_id=Obj_Id(), to_node_id=Obj_Id())

        node_ok_id = self.graph.new_node().node_id
        node_bad_id = Obj_Id()
        with pytest.raises(ValueError, match=f"To node {node_bad_id} not found"):
            self.graph.new_edge(from_node_id=node_ok_id, to_node_id=node_bad_id)

        with pytest.raises(ValueError, match=f"From node {node_bad_id} not found"):
            self.graph.new_edge(from_node_id=node_bad_id, to_node_id=node_ok_id)

    def test_custom_node_types(self):                                                       # Tests creation of nodes with custom types
        class Custom_Node(Simple_Node): pass

        default_node = self.graph.new_node()                                                # Create node with default type
        assert isinstance(default_node, Model__MGraph__Node)
        assert default_node.node_type == Simple_Node                                        # Should use default_node_type

        custom_node = self.graph.new_node(node_type=Custom_Node)                            # Create node with custom type
        assert isinstance(custom_node, Model__MGraph__Node)
        assert custom_node.node_type == Custom_Node

    def test_graph_queries(self):                                                           # Tests graph querying methods
        node_1 = self.graph.new_node()                                               # Add some test nodes
        node_2 = self.graph.new_node()
        node_3 = self.graph.new_node()
        nodes = list(self.graph.nodes())                                                    # Test nodes() method
        graph = self.graph.graph()                                                          # Test graph() method

        assert len(nodes)                               == 3
        assert node_1.json()                            == nodes[0].json()
        assert node_2.json()                            == nodes[1].json()
        assert node_3.json()                            == nodes[2].json()
        assert isinstance(graph, Schema__MGraph__Graph) is True
        assert len(graph.nodes)                         == 3
        assert len(graph.edges)                         == 0

    def test_edge_constraints(self):                                                        # Tests edge creation constraints
        class Another_Node(Simple_Node): pass                                      # Create nodes of different types
        
        node_1 = self.graph.new_node(node_type=Simple_Node )
        node_2 = self.graph.new_node(node_type=Another_Node)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id

        edge_1 = self.graph.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)                                   # Create edge between nodes

        assert type(edge_1)                              is Model__MGraph__Edge
        assert self.graph.delete_node(node_id=node_2_id) is True                                     # Test edge validation with deleted node
        assert self.graph.delete_node(node_id=node_2_id) is False

        with pytest.raises(ValueError, match=f"To node {node_2_id} not found"):
            self.graph.add_edge(edge_1.data)

        assert self.graph.delete_node(node_id=node_1_id) is True  # Test edge validation with deleted node
        assert self.graph.delete_node(node_id=node_1_id) is False

        with pytest.raises(ValueError, match=f"From node {node_1_id} not found"):
            self.graph.add_edge(edge_1.data)