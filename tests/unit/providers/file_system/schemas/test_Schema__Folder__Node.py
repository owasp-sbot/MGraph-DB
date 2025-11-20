from unittest                                                                    import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now
from mgraph_db.providers.file_system.schemas.Schema__File_System__Item           import Schema__File_System__Item
from mgraph_db.providers.file_system.schemas.Schema__Folder__Node                import Schema__Folder__Node

class test_Schema__Folder__Node(TestCase):

    def setUp(self):                                                                               # Initialize test data
        self.folder_name = "test_folder"
        self.created_at  = Timestamp_Now()
        self.modified_at = Timestamp_Now()
        self.folder_node = Schema__Folder__Node(folder_name  = self.folder_name     ,
                                                created_at   = self.created_at      ,
                                                modified_at  = self.modified_at     ,
                                                node_type    = Schema__Folder__Node )

    def test_init(self):                                                                          # Tests basic initialization and type checking
        assert type(self.folder_node)        is Schema__Folder__Node
        assert self.folder_node.folder_name  == self.folder_name
        assert self.folder_node.created_at   == self.created_at
        assert self.folder_node.modified_at  == self.modified_at

    def test_inheritance(self):                                                                   # Tests inheritance from File_System_Item
        assert isinstance(self.folder_node, Schema__File_System__Item)

