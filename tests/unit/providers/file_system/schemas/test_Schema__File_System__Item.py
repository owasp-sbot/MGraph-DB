import pytest
import re
from unittest                                                                    import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now
from mgraph_db.providers.file_system.schemas.Schema__File_System__Item           import Schema__File_System__Item

class test_Schema__File_System__Item(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):                                                                                # Initialize test data
        self.folder_name = "test_folder"
        self.created_at  = Timestamp_Now()
        self.modified_at = Timestamp_Now()
        self.node_id     = Obj_Id       ()
        self.fs_item     = Schema__File_System__Item(folder_name  = self.folder_name         ,
                                                     created_at   = self.created_at          ,
                                                     modified_at  = self.modified_at         ,
                                                     node_config  = None                     ,
                                                     node_type    = Schema__File_System__Item,
                                                     value        = None                     )

    def test_init(self):                                                                           # Tests basic initialization and type checking
        assert type(self.fs_item)           is Schema__File_System__Item
        assert self.fs_item.folder_name     == self.folder_name
        assert self.fs_item.created_at      == self.created_at
        assert self.fs_item.modified_at     == self.modified_at

    def test_type_safety_validation(self):                                                         # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__File_System__Item(folder_name  = 123,                                          # Should be str
                                      created_at   = self.created_at            ,
                                      modified_at  = self.modified_at           ,
                                      node_config  = None                       ,
                                      node_type    = Schema__File_System__Item  ,
                                      value        = None                       )
        assert 'Invalid type for attribute' in str(context.exception)

        with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'not-a-timestamp'")):
            Schema__File_System__Item(folder_name  = self.folder_name           ,
                                      created_at   = "not-a-timestamp"          ,                              # Should be Timestamp_Now
                                      modified_at  = self.modified_at           ,
                                      node_config  = None                       ,
                                      node_type    = Schema__File_System__Item  ,
                                      value        = None                       )

