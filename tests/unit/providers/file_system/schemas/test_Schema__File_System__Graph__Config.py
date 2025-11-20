import pytest
from unittest                                                                   import TestCase
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id


class test_Schema__File_System__Graph__Config(TestCase):

    def setUp(self):                                                                              # Initialize test data
        self.graph_id           = Obj_Id()
        self.allow_circular_refs = False
        self.graph_config       = Schema__File_System__Graph__Config(allow_circular_refs = self.allow_circular_refs)

    def test_init(self):                                                                         # Tests basic initialization and type checking
        assert type(self.graph_config)                is Schema__File_System__Graph__Config
        assert self.graph_config.allow_circular_refs  == self.allow_circular_refs

    def test_type_safety_validation(self):                                                       # Tests type safety validations
        with pytest.raises(ValueError, match="Invalid type for attribute 'allow_circular_refs'. Expected '<class 'bool'>' but got '<class 'str'>'"):
            Schema__File_System__Graph__Config(allow_circular_refs = "not-a-bool")                                                  # Should be bool


