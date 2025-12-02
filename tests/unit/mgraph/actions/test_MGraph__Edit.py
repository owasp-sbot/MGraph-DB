from unittest                                                       import TestCase
from mgraph_db.mgraph.MGraph                                        import MGraph
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.utils.Objects                                      import base_classes
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit                          import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index                         import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Custom__Node(Schema__MGraph__Node): pass                                                      # Helper classes for testing
class Custom__Edge(Schema__MGraph__Edge): pass


class test_MGraph__Edit(TestCase):

    @classmethod
    def setUpClass(cls):                                                                            # Use setUpClass for expensive setup
        cls.schema_graph = Schema__MGraph__Graph( nodes      = {}                    ,
                                                  edges      = {}                    ,
                                                  graph_type = Schema__MGraph__Graph )
        cls.model_graph  = Model__MGraph__Graph ( data       = cls.schema_graph      )
        cls.domain_graph = Domain__MGraph__Graph( model      = cls.model_graph       )

    def setUp(self):                                                                                # Fresh edit object for each test
        self.schema_graph = Schema__MGraph__Graph( nodes      = {}                    ,
                                                   edges      = {}                    ,
                                                   graph_type = Schema__MGraph__Graph )
        self.model_graph  = Model__MGraph__Graph ( data       = self.schema_graph     )
        self.domain_graph = Domain__MGraph__Graph( model      = self.model_graph      )
        self.graph_edit   = MGraph__Edit         ( graph      = self.domain_graph     )

    def test__init__(self):                                                                         # Test MGraph__Edit initialization
        with self.graph_edit as _:
            assert type(_)            is MGraph__Edit
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph)      is Domain__MGraph__Graph
            assert _.data_type        is MGraph__Data
            assert type(_.data_type)  is MGraph__Data.__class__
            assert type(_.data_type)  is type

    def test__init____with_data_type(self):                                                         # Test initialization with custom data_type
        with MGraph__Edit( graph     = self.domain_graph ,
                           data_type = MGraph__Data      ) as _:
            assert _.data_type is MGraph__Data


    # ---- Node Operations ----

    def test_new_node(self):                                                                        # Test creating a new node
        with self.graph_edit as _:
            node = _.new_node()

            assert type(node)         is Domain__MGraph__Node
            assert type(node.node_id) is Node_Id
            assert node.node_id       in _.graph.model.data.nodes                                   # Node is in graph

    def test_new_node__with_custom_type(self):                                                      # Test creating node with custom type
        with self.graph_edit as _:
            node = _.new_node(node_type=Custom__Node)

            assert node.node.data.node_type is Custom__Node

    def test_new_node__with_path(self):                                                             # Test creating node with path
        with self.graph_edit as _:
            node = _.new_node(node_path=Node_Path("test.node.path"))

            assert node.node.data.node_path == Node_Path("test.node.path")
            assert node.node_id in _.index().get_nodes_by_path(Node_Path("test.node.path"))

    def test_new_node__indexed(self):                                                               # Test that new node is added to index
        with self.graph_edit as _:
            node      = _.new_node() #.set_node_type()
            node_type = node.node.data.node_type
            assert node_type    is None
            assert node.node_id in _.index().get_nodes_by_type(Schema__MGraph__Node)

    def test_add_node(self):                                                                        # Test adding a pre-created node
        with self.graph_edit as _:
            schema_node = Schema__MGraph__Node()
            result      = _.add_node(schema_node)

            assert type(result)       is Domain__MGraph__Node
            assert result.node_id     == schema_node.node_id
            assert schema_node.node_id in _.graph.model.data.nodes


    # ---- Edge Operations ----

    def test_new_edge(self):                                                                        # Test creating a new edge
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            assert type(edge)         is Domain__MGraph__Edge
            assert type(edge.edge_id) is Edge_Id
            assert edge.from_node_id()== node_1.node_id
            assert edge.to_node_id()  == node_2.node_id
            assert edge.edge_id       in _.graph.model.data.edges                                   # Edge is in graph

    def test_new_edge__with_custom_type(self):                                                      # Test creating edge with custom type
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge( from_node_id = node_1.node_id ,
                                 to_node_id   = node_2.node_id ,
                                 edge_type    = Custom__Edge   )

            assert edge.edge.data.edge_type is Custom__Edge

    def test_new_edge__with_path(self):                                                             # Test creating edge with path
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge( from_node_id = node_1.node_id                  ,
                                 to_node_id   = node_2.node_id                  ,
                                 edge_path    = Edge_Path("test.edge.path")     )

            assert edge.edge.data.edge_path == Edge_Path("test.edge.path")
            assert edge.edge_id in _.index().get_edges_by_path(Edge_Path("test.edge.path"))

    def test_new_edge__indexed(self):                                                               # Test that new edge is added to index
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            assert edge.edge_id in _.index().get_edges_by_type(Schema__MGraph__Edge)

    def test_add_edge(self):                                                                        # Test adding a pre-created edge
        with self.graph_edit as _:
            node_1      = _.new_node()
            node_2      = _.new_node()
            schema_edge = Schema__MGraph__Edge( from_node_id = node_1.node_id ,
                                                to_node_id   = node_2.node_id )
            result      = _.add_edge(schema_edge)

            assert type(result)        is Domain__MGraph__Edge
            assert result.edge_id      == schema_edge.edge_id
            assert schema_edge.edge_id in _.graph.model.data.edges


    # ---- Connect Nodes ----

    def test_connect_nodes(self):                                                                   # Test connecting two domain nodes
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.connect_nodes(from_node=node_1, to_node=node_2)

            assert type(edge)           is Domain__MGraph__Edge
            assert edge.from_node_id()  == node_1.node_id
            assert edge.to_node_id()    == node_2.node_id

    def test_connect_nodes__with_edge_type(self):                                                   # Test connecting nodes with custom edge type
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.connect_nodes(from_node=node_1, to_node=node_2, edge_type=Custom__Edge)

            assert edge.edge.data.edge_type is Custom__Edge

    def test_connect_nodes__indexed(self):                                                          # Test that connected edge is indexed
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.connect_nodes(from_node=node_1, to_node=node_2)

            assert edge.edge_id in _.index().edges_to_nodes()


    # ---- Create Edge (convenience method) ----

    def test_create_edge(self):                                                                     # Test create_edge convenience method
        with self.graph_edit as _:
            result = _.create_edge()

            assert type(result)           is dict
            assert 'node_1' in result
            assert 'node_2' in result
            assert 'edge_1' in result
            assert type(result['node_1']) is Domain__MGraph__Node
            assert type(result['node_2']) is Domain__MGraph__Node
            assert type(result['edge_1']) is Domain__MGraph__Edge

            edge = result['edge_1']
            assert edge.from_node_id() == result['node_1'].node_id
            assert edge.to_node_id()   == result['node_2'].node_id


    # ---- Get or Create Edge ----

    def test_get_or_create_edge__creates_new(self):                                                 # Test get_or_create_edge creates new edge
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge   = _.get_or_create_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            assert type(edge)          is Domain__MGraph__Edge
            assert edge.from_node_id() == node_1.node_id
            assert edge.to_node_id()   == node_2.node_id

    def test_get_or_create_edge__returns_existing(self):                                            # Test get_or_create_edge returns existing edge
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.get_or_create_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            assert edge_1.edge_id == edge_2.edge_id                                                 # Same edge returned

    def test_get_or_create_edge__with_edge_type(self):                                              # Test get_or_create_edge with custom edge type
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge_1  = _.new_edge( from_node_id = node_1.node_id ,
                                  to_node_id   = node_2.node_id ,
                                  edge_type    = Custom__Edge   )
            edge_2  = _.get_or_create_edge( from_node_id = node_1.node_id ,
                                            to_node_id   = node_2.node_id ,
                                            edge_type    = Custom__Edge   )

            assert edge_1.edge_id == edge_2.edge_id

    def test_get_or_create_edge__different_type_creates_new(self):                                  # Test that different edge type creates new edge
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge_1  = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)            # Default type
            edge_2  = _.get_or_create_edge( from_node_id = node_1.node_id ,                         # Custom type
                                            to_node_id   = node_2.node_id ,
                                            edge_type    = Custom__Edge   )

            assert edge_1.edge_id != edge_2.edge_id                                                 # Different edges


    # ---- Value Nodes ----

    def test_new_value(self):                                                                       # Test creating a value node
        with self.graph_edit as _:
            node = _.new_value(42)

            assert type(node)                  is Domain__MGraph__Node
            assert node.node_data.value        == "42"                                              # Value stored as string
            assert node.node_data.value_type   is int                                               # Type preserved

    def test_new_value__reuses_existing(self):                                                      # Test that new_value reuses existing node
        with self.graph_edit as _:
            node_1 = _.new_value(42)
            node_2 = _.new_value(42)

            assert node_1.node_id == node_2.node_id                                                 # Same node returned

    def test_new_value__different_values_create_new(self):                                          # Test that different values create new nodes
        with self.graph_edit as _:
            node_1 = _.new_value(42)
            node_2 = _.new_value(43)

            assert node_1.node_id != node_2.node_id                                                 # Different nodes

    def test_new_value__different_types_create_new(self):                                           # Test that same value but different types create new nodes
        with self.graph_edit as _:
            node_1 = _.new_value(42)                                                                # int
            node_2 = _.new_value("42")                                                              # str

            assert node_1.node_id != node_2.node_id
            assert node_1.node_data.value_type is int
            assert node_2.node_data.value_type is str

    def test_new_value__with_key(self):                                                             # Test creating value node with unique key
        with self.graph_edit as _:
            node_1 = _.new_value(42, key="key_1")
            node_2 = _.new_value(42, key="key_2")

            assert node_1.node_id != node_2.node_id                                                 # Different keys create different nodes

    def test_new_value__with_path(self):                                                            # Test creating value node with path
        with self.graph_edit as _:
            node = _.new_value(42, node_path=Node_Path("value.node.path"))

            assert node.node.data.node_path == Node_Path("value.node.path")


    # ---- Path Operations ----

    def test_set_node_path(self):                                                                   # Test setting a node's path
        with self.graph_edit as _:
            node    = _.new_node()
            node_id = node.node_id

            assert node.node.data.node_path is None                                                 # Initially no path

            result = _.set_node_path(node_id, Node_Path("new.path"))
            assert result is True

            updated_node = _.data().node(node_id)
            assert updated_node.node.data.node_path == Node_Path("new.path")
            assert node_id in _.index().get_nodes_by_path(Node_Path("new.path"))

    def test_set_node_path__updates_index(self):                                                    # Test that set_node_path updates index correctly
        with self.graph_edit as _:
            node    = _.new_node(node_path=Node_Path("old.path"))
            node_id = node.node_id

            assert node_id in _.index().get_nodes_by_path(Node_Path("old.path"))

            _.set_node_path(node_id, Node_Path("new.path"))

            assert node_id not in _.index().get_nodes_by_path(Node_Path("old.path"))                # Removed from old
            assert node_id     in _.index().get_nodes_by_path(Node_Path("new.path"))                # Added to new

    def test_set_node_path__clear_path(self):                                                       # Test clearing a node's path
        with self.graph_edit as _:
            node    = _.new_node(node_path=Node_Path("existing.path"))
            node_id = node.node_id

            result = _.set_node_path(node_id, '')
            assert result is True

            updated_node = _.data().node(node_id)
            assert updated_node.node.data.node_path == ''
            assert node_id not in _.index().get_nodes_by_path(Node_Path("existing.path"))

    def test_set_node_path__nonexistent_node(self):                                                 # Test setting path on nonexistent node
        with self.graph_edit as _:
            fake_node_id = Node_Id()
            result       = _.set_node_path(fake_node_id, Node_Path("some.path"))

            assert result is False

    def test_set_edge_path(self):                                                                   # Test setting an edge's path
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_id = edge.edge_id

            assert edge.edge.data.edge_path is None                                                 # Initially no path

            result = _.set_edge_path(edge_id, Edge_Path("new.edge.path"))
            assert result is True

            updated_edge = _.data().edge(edge_id)
            assert updated_edge.edge.data.edge_path == Edge_Path("new.edge.path")
            assert edge_id in _.index().get_edges_by_path(Edge_Path("new.edge.path"))

    def test_set_edge_path__updates_index(self):                                                    # Test that set_edge_path updates index correctly
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge( from_node_id = node_1.node_id         ,
                                  to_node_id   = node_2.node_id         ,
                                  edge_path    = Edge_Path("old.path")  )
            edge_id = edge.edge_id

            assert edge_id in _.index().get_edges_by_path(Edge_Path("old.path"))

            _.set_edge_path(edge_id, Edge_Path("new.path"))

            assert edge_id not in _.index().get_edges_by_path(Edge_Path("old.path"))                # Removed from old
            assert edge_id     in _.index().get_edges_by_path(Edge_Path("new.path"))                # Added to new

    def test_set_edge_path__nonexistent_edge(self):                                                 # Test setting path on nonexistent edge
        with self.graph_edit as _:
            fake_edge_id = Edge_Id()
            result       = _.set_edge_path(fake_edge_id, Edge_Path("some.path"))

            assert result is False


    # ---- Deletion Operations ----

    def test_delete_node(self):                                                                     # Test deleting a node
        with self.graph_edit as _:
            node    = _.new_node()
            node_id = node.node_id

            assert node_id in _.graph.model.data.nodes                                              # Node exists

            result = _.delete_node(node_id)
            assert result is True

            assert node_id not in _.graph.model.data.nodes                                          # Node removed

    def test_delete_node__removes_from_index(self):                                                 # Test that delete_node removes from index
        with self.graph_edit as _:
            node    = _.new_node(node_path=Node_Path("to.be.deleted"))
            node_id = node.node_id

            assert node_id in _.index().get_nodes_by_path(Node_Path("to.be.deleted"))

            _.delete_node(node_id)

            assert node_id not in _.index().get_nodes_by_path(Node_Path("to.be.deleted"))

    def test_delete_node__nonexistent(self):                                                        # Test deleting nonexistent node
        with self.graph_edit as _:
            fake_node_id = Node_Id()
            result       = _.delete_node(fake_node_id)

            assert result is False

    def test_delete_node__removes_connected_edges(self):                                            # Test that deleting node removes connected edges
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_id = edge.edge_id

            assert edge_id in _.graph.model.data.edges                                              # Edge exists

            _.delete_node(node_1.node_id)

            assert edge_id not in _.graph.model.data.edges                                          # Edge removed

    def test_delete_edge(self):                                                                     # Test deleting an edge
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_id = edge.edge_id

            assert edge_id in _.graph.model.data.edges                                              # Edge exists

            result = _.delete_edge(edge_id)
            assert result is True

            assert edge_id not in _.graph.model.data.edges                                          # Edge removed

    def test_delete_edge__removes_from_index(self):                                                 # Test that delete_edge removes from index
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge( from_node_id = node_1.node_id              ,
                                  to_node_id   = node_2.node_id              ,
                                  edge_path    = Edge_Path("to.be.deleted")  )
            edge_id = edge.edge_id

            assert edge_id in _.index().get_edges_by_path(Edge_Path("to.be.deleted"))

            _.delete_edge(edge_id)

            assert edge_id not in _.index().get_edges_by_path(Edge_Path("to.be.deleted"))

    def test_delete_edge__nonexistent(self):                                                        # Test deleting nonexistent edge
        with self.graph_edit as _:
            fake_edge_id = Edge_Id()
            result       = _.delete_edge(fake_edge_id)

            assert result is False

    def test_delete_edge__preserves_nodes(self):                                                    # Test that deleting edge preserves nodes
        with self.graph_edit as _:
            node_1  = _.new_node()
            node_2  = _.new_node()
            edge    = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

            _.delete_edge(edge.edge_id)

            assert node_1.node_id in _.graph.model.data.nodes                                       # Nodes still exist
            assert node_2.node_id in _.graph.model.data.nodes


    # ---- Accessor Methods ----

    def test_data(self):                                                                            # Test data() accessor
        with MGraph__Edit( graph     = self.domain_graph ,
                           data_type = MGraph__Data      ) as _:
            data = _.data()

            assert type(data) is MGraph__Data
            assert data       is _.data()                                                           # Cached - same object

    def test_index(self):                                                                           # Test index() accessor
        with self.graph_edit as _:
            index = _.index()

            assert type(index) is MGraph__Index
            assert index       is _.index()                                                         # Cached - same object


    # ---- Integration Tests ----

    def test__integration__complex_graph(self):                                                     # Test building a complex graph
        with self.graph_edit as _:
            node_a = _.new_node(node_path=Node_Path("root"))
            node_b = _.new_node(node_path=Node_Path("root.child"))
            node_c = _.new_node(node_path=Node_Path("root.child"))
            node_d = _.new_node(node_path=Node_Path("root.other"))

            edge_ab = _.connect_nodes(from_node=node_a, to_node=node_b)
            edge_ac = _.connect_nodes(from_node=node_a, to_node=node_c)
            edge_ad = _.connect_nodes(from_node=node_a, to_node=node_d)
            edge_bc = _.connect_nodes(from_node=node_b, to_node=node_c)

            assert len(_.graph.model.data.nodes) == 4                                               # Verify counts
            assert len(_.graph.model.data.edges) == 4

            root_nodes  = _.index().get_nodes_by_path(Node_Path("root"))                            # Verify path indexing
            child_nodes = _.index().get_nodes_by_path(Node_Path("root.child"))
            other_nodes = _.index().get_nodes_by_path(Node_Path("root.other"))

            assert len(root_nodes)  == 1
            assert len(child_nodes) == 2                                                            # Two nodes share this path
            assert len(other_nodes) == 1

    def test__integration__value_graph(self):                                                       # Test building a graph with value nodes
        with self.graph_edit as _:
            int_node  = _.new_value(42)
            str_node  = _.new_value("hello")
            bool_node = _.new_value(True)

            _.connect_nodes(from_node=int_node,  to_node=str_node)
            _.connect_nodes(from_node=str_node,  to_node=bool_node)
            _.connect_nodes(from_node=bool_node, to_node=int_node)                                  # Circular reference

            assert len(_.graph.model.data.nodes) == 3
            assert len(_.graph.model.data.edges) == 3

            int_node_2 = _.new_value(42)                                                            # Same value reuses node
            assert int_node.node_id == int_node_2.node_id


    # =============================================================================
    # rebuild_index Tests
    # =============================================================================

    def test_rebuild_index__returns_fresh_index(self):                           # Test rebuild returns new index
        with self.graph_edit as _:
            node = _.new_node()

            index_1 = _.index()
            index_2 = _.rebuild_index()

            assert type(index_2) is MGraph__Index
            assert index_1       is not index_2                                  # Different objects

    def test_rebuild_index__reflects_current_state(self):                        # Test rebuild reflects graph state
        with self.graph_edit as _:
            node_1 = _.new_node(node_path=Node_Path("initial"))

            initial_index = _.index()
            assert node_1.node_id in initial_index.get_nodes_by_path(Node_Path("initial"))

            node_2 = _.new_node(node_path=Node_Path("added"))

            rebuilt_index = _.rebuild_index()

            assert node_1.node_id in rebuilt_index.get_nodes_by_path(Node_Path("initial"))
            assert node_2.node_id in rebuilt_index.get_nodes_by_path(Node_Path("added"))

    def test_rebuild_index__clears_cache(self):                                  # Test that cache is properly cleared
        with self.graph_edit as _:
            _ .new_node()
            index_before = _.index()

            _.rebuild_index()

            index_after = _.index()

            assert index_before != index_after
            assert index_before is not index_after                               # Cache was cleared

    # =============================================================================
    # get_or_create_edge with Predicate Tests
    # =============================================================================

    def test_get_or_create_edge__with_predicate__creates_new(self):              # Test creating edge with predicate
        with self.graph_edit as _:
            node_1 = _.new_node()
            node_2 = _.new_node()

            edge = _.get_or_create_edge(from_node_id = node_1.node_id   ,
                                        to_node_id   = node_2.node_id   ,
                                        predicate    = 'test_predicate' )

            assert type(edge) is Domain__MGraph__Edge

    def test_get_or_create_edge__with_predicate__returns_existing(self):         # Test returning existing edge with matching predicate
        with self.graph_edit as _:
            from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label import Schema__MGraph__Edge__Label

            node_1 = _.new_node()
            node_2 = _.new_node()

            edge_label = Schema__MGraph__Edge__Label(predicate=Safe_Id('my_pred'))
            edge_1     = _.new_edge(from_node_id = node_1.node_id ,
                                    to_node_id   = node_2.node_id )

            edge_1.edge.data.edge_label = edge_label

            _.index().add_edge_label(edge_1.edge.data)

            edge_2 = _.get_or_create_edge(from_node_id = node_1.node_id ,
                                          to_node_id   = node_2.node_id ,
                                          predicate    = 'my_pred'      )

            assert edge_1.edge_id == edge_2.edge_id

    # =============================================================================
    # Integration Tests
    # =============================================================================

    def test_full_workflow_with_paths_and_predicates(self):                      # Test complete workflow
        mgraph = MGraph()

        with mgraph.edit() as edit:
            root     = edit.new_node(node_path=Node_Path("root"))
            child_1  = edit.new_node(node_path=Node_Path("root.children"))
            child_2  = edit.new_node(node_path=Node_Path("root.children"))
            leaf     = edit.new_node(node_path=Node_Path("root.children.leaf"))

            from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label import Schema__MGraph__Edge__Label

            label_has_child = Schema__MGraph__Edge__Label(predicate=Safe_Id('has_child'))

            edge_1 = edit.new_edge(from_node_id = root.node_id   ,
                                   to_node_id   = child_1.node_id,
                                   edge_path    = Edge_Path("root.edges"))
            edge_1.edge.data.edge_label = label_has_child
            edit.index().add_edge_label(edge_1.edge.data)

            edge_2 = edit.new_edge(from_node_id = root.node_id   ,
                                   to_node_id   = child_2.node_id,
                                   edge_path    = Edge_Path("root.edges"))
            edge_2.edge.data.edge_label = label_has_child
            edit.index().add_edge_label(edge_2.edge.data)

            edit.connect_nodes(from_node=child_1, to_node=leaf)

        with mgraph.index() as index:
            all_node_paths = index.get_all_node_paths()
            assert len(all_node_paths) == 3                                      # root, root.children, root.children.leaf

            children = index.get_nodes_by_path(Node_Path("root.children"))
            assert len(children) == 2                                            # Two children at same path

            root_children = index.get_nodes_by_predicate(root.node_id, Safe_Id('has_child'))
            assert len(root_children) == 2                                       # Two children via predicate

            stats = index.stats()
            assert stats['summary']['total_nodes']       == 4
            assert stats['summary']['unique_node_paths'] == 3
            assert stats['summary']['total_predicates']  == 1

    def test_rebuild_after_modifications(self):                                  # Test rebuild reflects changes
        mgraph = MGraph()

        with mgraph.edit() as edit:
            node = edit.new_node(node_path=Node_Path("original"))

            index_1 = edit.index()
            assert node.node_id in index_1.get_nodes_by_path(Node_Path("original"))

            edit.set_node_path(node.node_id, Node_Path("modified"))

            index_2 = edit.rebuild_index()

            assert node.node_id     in index_2.get_nodes_by_path(Node_Path("modified"))
            assert node.node_id not in index_2.get_nodes_by_path(Node_Path("original"))

    def test_mgraph_index__accessor(self):                                       # Test MGraph.index() works
        mgraph = MGraph()

        with mgraph.edit() as edit:
            node = edit.new_node(node_path=Node_Path("test"))

        with mgraph.index() as index:
            assert type(index) is MGraph__Index
            assert node.node_id in index.get_nodes_by_path(Node_Path("test"))
