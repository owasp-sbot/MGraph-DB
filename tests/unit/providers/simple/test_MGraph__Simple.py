from unittest                                                       import TestCase
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_db.providers.simple.models.Model__Simple__Graph         import Model__Simple__Graph
from mgraph_db.providers.simple.models.Model__Simple__Node          import Model__Simple__Node
from mgraph_db.providers.simple.models.Model__Simple__Types         import Model__Simple__Types
from mgraph_db.providers.simple.schemas.Schema__Simple__Graph       import Schema__Simple__Graph
from mgraph_db.providers.simple.schemas.Schema__Simple__Node        import Schema__Simple__Node
from mgraph_db.providers.simple.schemas.Schema__Simple__Node__Data  import Schema__Simple__Node__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Objects                                      import base_types, type_full_name
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit                          import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Export                        import MGraph__Export
from mgraph_db.providers.simple.MGraph__Simple                      import MGraph__Simple
from mgraph_db.providers.simple.domain.Domain__Simple__Graph        import Domain__Simple__Graph


class test_MGraph__Simple(TestCase):

    def setUp(self):                                                            # Initialize MGraph__Simple instance
        self.mgraph_simple = MGraph__Simple()

    def test_init(self):                                                        # Test basic initialization
        with self.mgraph_simple as _:
            assert type(_)                                 is MGraph__Simple
            assert base_types(_)                           == [MGraph, Type_Safe, object]
            assert type(self.mgraph_simple.graph)          is Domain__Simple__Graph
            assert base_types(self.mgraph_simple.graph)    == [Domain__MGraph__Graph, Type_Safe, object]

    def test_data(self):                                                        # Test data method returns correct type
        with self.mgraph_simple.data() as _:
            assert type(_) is MGraph__Data

    def test_edit(self):                                                        # Test edit method returns correct type
        with self.mgraph_simple.edit() as _:
            assert type(_) is MGraph__Edit

    def test_export(self):                                                      # Test export method returns correct type
        with self.mgraph_simple.export() as _:
            assert type(_) is MGraph__Export

    def test_edit_new_node(self):                                               # Test creating a new node
        with self.mgraph_simple.edit() as edit:
            node     = edit.new_node()
            node_id  = node.node_id
            graph_id = edit.graph.graph_id()
            assert node            is not None                                                                 # Verify node creation
            assert type(node_id  ) is Obj_Id
            assert type(node.node) is Model__Simple__Node
            assert type(node.node) is self.mgraph_simple.graph.model.model_types.node_model_type
            assert node.node_id    in self.mgraph_simple.graph.model.data.nodes                                 # Verify node is in graph

            assert type(self.mgraph_simple                        ) is MGraph__Simple                           # check type
            assert type(self.mgraph_simple.graph                  ) is Domain__Simple__Graph
            assert type(self.mgraph_simple.graph.model            ) is Model__Simple__Graph
            assert type(self.mgraph_simple.graph.model.model_types) is Model__Simple__Types
            assert type(self.mgraph_simple.graph.model.data       ) is Schema__Simple__Graph

            assert node.json() == {'graph': {'data'                 : {'edges'       : {},
                                                                       'graph_data'  : {},
                                                                       'graph_id'    : graph_id,
                                                                       'graph_type'  : type_full_name(Schema__Simple__Graph),
                                                                       'nodes'       : { node_id: { 'node_data': {'name' : None ,
                                                                                                                  'value': None},
                                                                                                    'node_id'  : node_id,
                                                                                                    'node_type' : type_full_name(Schema__Simple__Node    )}},
                                                                       'schema_types': {'edge_type'       : type_full_name(Schema__MGraph__Edge         ),
                                                                                        'graph_data_type' : type_full_name(Schema__MGraph__Graph__Data  ),
                                                                                        'node_data_type'  : type_full_name(Schema__Simple__Node__Data   ),
                                                                                        'node_type'       : type_full_name(Schema__Simple__Node         )}},
                                             'model_types'          : {'edge_model_type' : type_full_name(Model__MGraph__Edge          ),
                                                                       'node_model_type' : type_full_name(Model__Simple__Node          )}},
                                   'node': {'data': {'node_data': {'name': None, 'value': None}         ,
                                                     'node_id'  : node_id                               ,
                                                     'node_type': type_full_name(Schema__Simple__Node)  }}}


    def test_edit_new_node_with_value(self):                                    # Test creating a node with specific value
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(value='test_value')                            # create a new node with the node data 'value' field set
            assert node.node_data.value == 'test_value'                         # confirm the node data was set

    def test_edit_new_node_with_name(self):                                     # Test creating a node with specific name
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(name='test_name')

            # Verify node name
            assert node.node_data.name == 'test_name'

    def test_edit_new_edge(self):                                               # Test creating an edge between nodes
        with self.mgraph_simple.edit() as edit:
            node1 = edit.new_node(value='node1')
            node2 = edit.new_node(value='node2')

            # Create edge
            edge = edit.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)

            # Verify edge creation
            assert edge is not None
            assert type(edge.edge) is self.mgraph_simple.graph.model.model_types.edge_model_type

            # Verify edge is in graph
            assert edge.edge_id in self.mgraph_simple.graph.model.data.edges

    def test_data_method_node_retrieval(self):                                  # Test retrieving nodes via data method
        with self.mgraph_simple.edit() as edit:
            # Create some nodes
            node1 = edit.new_node(value='node1')
            node2 = edit.new_node(value='node2')

        # Retrieve nodes
        with self.mgraph_simple.data() as data:
            all_nodes = data.nodes()

            # Verify nodes can be retrieved
            assert len(all_nodes) == 2
            assert any(node.node_data.value == 'node1' for node in all_nodes)
            assert any(node.node_data.value == 'node2' for node in all_nodes)

    def test_node_multiple_operations(self):                                    # Test multiple node and edge operations
        with self.mgraph_simple.edit() as edit:
            # Create multiple nodes
            root = edit.new_node(name='root')
            child1 = edit.new_node(value='child1')
            child2 = edit.new_node(value='child2')

            # Create edges
            edge1 = edit.new_edge(from_node_id=root.node_id, to_node_id=child1.node_id)
            edge2 = edit.new_edge(from_node_id=root.node_id, to_node_id=child2.node_id)

            # Verify multiple operations
            assert len(self.mgraph_simple.graph.model.data.nodes) == 3
            assert len(self.mgraph_simple.graph.model.data.edges) == 2

    def test_json_serialization(self):                                          # Test JSON serialization
        with self.mgraph_simple.edit() as edit:
            # Create some nodes
            node1 = edit.new_node(value='node1')
            node2 = edit.new_node(value='node2')

        # Serialize to JSON
        json_data = self.mgraph_simple.json()
        assert isinstance(json_data, dict)

    def test_json_deserialization(self):                                        # Test JSON deserialization
        with self.mgraph_simple.edit() as edit:
            # Create some nodes
            node1 = edit.new_node(value='node1')
            node2 = edit.new_node(value='node2')

        # Serialize to JSON
        json_data = self.mgraph_simple.json()

        # Create new instance from JSON
        restored_mgraph = MGraph__Simple.from_json(json_data)

        # Verify restored graph
        assert type(restored_mgraph) is MGraph__Simple
        with restored_mgraph.data() as data:
            all_nodes = data.nodes()
            assert len(all_nodes) == 2
            assert any(node.node_data.value == 'node1' for node in all_nodes)
            assert any(node.node_data.value == 'node2' for node in all_nodes)