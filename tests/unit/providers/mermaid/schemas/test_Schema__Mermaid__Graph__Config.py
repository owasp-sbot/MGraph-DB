import re
import pytest
from unittest                                                            import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Types          import Schema__Mermaid__Types
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config

class test_Schema__Mermaid__Graph__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.schema_types  = Schema__Mermaid__Types()
        self.graph_config  = Schema__Mermaid__Graph__Config(allow_circle_edges   = True       ,
                                                            allow_duplicate_edges= False      ,
                                                            graph_title         = "Test Graph")

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.graph_config)                 is Schema__Mermaid__Graph__Config
        assert self.schema_types.graph_data_type       is Schema__Mermaid__Graph__Config
        assert self.graph_config.allow_circle_edges    is True
        assert self.graph_config.allow_duplicate_edges is False
        assert self.graph_config.graph_title           == "Test Graph"


    def test_type_safety_validation(self):                                          # Tests type safety validations
        error_message = "On Schema__Mermaid__Graph__Config, invalid type for attribute 'graph_title'. Expected '<class 'str'>' but got '<class 'int'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Schema__Mermaid__Graph__Config(allow_circle_edges   = True ,
                                           allow_duplicate_edges= False,
                                           graph_title          = 123  ) # Invalid type for title


