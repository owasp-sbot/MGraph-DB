from unittest                                                                   import TestCase
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config
from osbot_utils.testing.__                                                     import __
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_db.providers.file_system.schemas.Schema__File_System__Types         import Schema__File_System__Types
from mgraph_db.providers.file_system.models.Model__File_System__Default_Types   import Model__File_System__Default_Types
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph         import Schema__File_System__Graph
from mgraph_db.mgraph.models.Model__MGraph__Edge                                import Model__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from mgraph_db.providers.file_system.models.Model__File_System__Graph           import Model__File_System__Graph
from mgraph_db.providers.file_system.models.Model__Folder__Node                 import Model__Folder__Node
from mgraph_db.providers.file_system.schemas.Schema__Folder__Node               import Schema__Folder__Node


class test_Model__File_System__Graph(TestCase):

    def setUp(self):                                                                                   # Initialize test data
        self.model = Model__File_System__Graph()

    def test_init(self):                                                                              # Tests basic initialization
        assert type(self.model                             ) is Model__File_System__Graph
        assert type(self.model.data                        ) is Schema__File_System__Graph
        assert type(self.model.data.schema_types)            is Schema__File_System__Types
        assert      self.model.data.schema_types.node_type   is Schema__Folder__Node
        assert      self.model.data.schema_types.edge_type   is None
        assert type(self.model.data.graph_data             ) is Schema__File_System__Graph__Config                                 # BUG
        assert type(self.model.model_types                 ) is Model__File_System__Default_Types
        assert      self.model.model_types.node_model_type   is Model__Folder__Node

        assert self.model.allow_circular_refs()             is False

        assert Schema__File_System__Types()                   .obj() == __(graph_data_type = 'mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config.Schema__File_System__Graph__Config',
                                                                           node_type       = 'mgraph_db.providers.file_system.schemas.Schema__Folder__Node.Schema__Folder__Node',
                                                                           node_data_type  = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data',
                                                                           edge_type       = None                                                                              )
        assert Schema__File_System__Graph(graph_id='07ee500d').obj()   == __(edges=__(),
                                                                             graph_data=__(allow_circular_refs=False),
                                                                             graph_id='07ee500d',
                                                                             nodes=__(),
                                                                             schema_types=__(graph_data_type='mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config.Schema__File_System__Graph__Config',
                                                                                             node_type='mgraph_db.providers.file_system.schemas.Schema__Folder__Node.Schema__Folder__Node',
                                                                                             node_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data',
                                                                                             edge_type=None),
                                                                             graph_path=None,
                                                                             graph_type=None)


    def test_new_edge(self):
        with self.model as _:
            node_1_id = _.new_node().node_id
            node_2_id = _.new_node().node_id
            edge      = _.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)

            #assert _.model_types.edge_model_type  is Model__MGraph__Edge
            #assert _.data.schema_types.edge_type  is Schema__MGraph__Edge
            assert type(edge)                     is Model__MGraph__Edge
            assert edge.obj() == __(data         = __(edge_data=None,
                                    edge_type    = 'mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                    edge_label   =  None,
                                    edge_path    =  None,
                                    from_node_id = node_1_id,
                                    to_node_id   = node_2_id,
                                    edge_id      = edge.edge_id()))

    def test_new_node(self):
        with self.model as _:
            assert type(_)                         is Model__File_System__Graph
            assert _.model_types.node_model_type   is Model__Folder__Node
            assert _.data.schema_types.node_type   is Schema__Folder__Node
            return
            node = _.new_node()
            assert type(node)                      is Model__Folder__Node

    def test__bug__cycle_detection__is_not_working(self):                                                                   # Tests cycle detection
        # Create nodes
        node1 = self.model.new_node(folder_name="folder1")
        node2 = self.model.new_node(folder_name="folder2")
        node3 = self.model.new_node(folder_name="folder3")

        # Test valid tree structure
        self.model.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
        self.model.new_edge(from_node_id=node2.node_id, to_node_id=node3.node_id)

        assert self.model.validate_no_cycles(node1.node_id, node3.node_id) is True

        # Test cycle detection
        # with self.assertRaises(ValueError) as context:
        #     self.model.new_edge(from_node_id=node3.node_id, to_node_id=node1.node_id)      # BUG: this is not being detected
        #     self.model.new_edge(from_node_id=node1.node_id, to_node_id=node3.node_id)      # BUG: we should also pick up this one this is correctly pickup by accident
        # assert "create a cycle" in str(context.exception)


        # Test with circular refs allowed
        self.model.set_allow_circular_refs(True)

        assert len(self.model.edges()) == 2
        self.model.new_edge(from_node_id=node3.node_id, to_node_id=node1.node_id)               # Should work, but not because the check is in place
        assert len(self.model.edges()) == 3


    def test__regression__base_class_none_prevents_object_creation(self):
        from osbot_utils.type_safe.primitives.core.Safe_Str                     import Safe_Str

        class Base_Class(Type_Safe):
            an_str : Safe_Str = None                        # BUG: this is preventing creation

        class With_Base(Base_Class):
            an_str : Safe_Str                               # BUG: this should have been created

        class An_Class(Type_Safe):
            an_str : Safe_Str

        assert An_Class  ().json() == {'an_str': ''}
        assert An_Class  ().obj () == __(an_str='')
        assert Base_Class().json() == {'an_str': None}
        assert Base_Class().obj () == __(an_str=None)
        # assert With_Base ().json() == {'an_str': None}      # BUG
        # assert With_Base ().obj () == __(an_str=None)       # BUG
        assert With_Base ().json() == {'an_str': ''}         # FIXED
        assert With_Base ().obj () == __(an_str='')