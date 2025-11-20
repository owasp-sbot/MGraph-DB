import pytest
from unittest                                                                    import TestCase
from osbot_utils.testing.__                                                      import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import is_obj_id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now
from osbot_utils.utils.Objects                                                   import full_type_name
from mgraph_db.providers.file_system.models.Model__File_System__Item             import Model__File_System__Item
from mgraph_db.providers.file_system.schemas.Schema__File_System__Item           import Schema__File_System__Item
from osbot_utils.utils.Misc                                                      import random_string, timestamp_utc_now


class test_Model__File_System__Item(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):                                                                                    # Initialize test data
        self.folder_name = random_string()
        self.item        = Schema__File_System__Item(folder_name = self.folder_name)
        self.model       = Model__File_System__Item (data        = self.item       )

    def test_init(self):                                                                               # Tests basic initialization
        timestamp_now = timestamp_utc_now()
        node_id       = self.model.node_id    ()
        created_at    = self.model.created_at
        modified_at   = self.model.modified_at
        node_type     = full_type_name(self.model.data.node_type)
        assert type(self.model)                 is Model__File_System__Item
        assert self.model.data.node_type        is Schema__File_System__Item
        assert self.model.folder_name           == self.folder_name
        assert self.model.created_at            is not None
        assert self.model.modified_at           is not None
        assert is_obj_id(node_id)               is True
        assert type(created_at)                 is Timestamp_Now
        assert type(modified_at)                is Timestamp_Now
        assert isinstance(created_at, int)      is True
        assert timestamp_now - 5 <= modified_at <= timestamp_now
        assert timestamp_now - 5 <= created_at  <= timestamp_now
        assert self.model.obj()                 == __(data=__(folder_name  = self.folder_name       ,
                                                             created_at  = created_at               ,
                                                             modified_at = modified_at              ,
                                                             node_config = __(node_id     = node_id,
                                                                              value_type  = None   ),
                                                             node_type   = node_type                ,
                                                             value       = None                     ))

    def test_set_folder_name(self):                                                                    # Tests folder name modification
        new_name = random_string()
        self.model.folder_name = new_name
        assert self.model.folder_name == new_name

    def test_update_modified_at(self):                                                                 # Tests timestamp updates
        original_time = self.model.modified_at
        self.model.modified_at = Timestamp_Now() + 2
        assert self.model.modified_at != original_time




