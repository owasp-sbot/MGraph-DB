import re
import pytest
from unittest                                            import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class test_Schema__MGraph__Node(TestCase):

    def setUp(self):    # Initialize test data
        self.node_data  = Schema__MGraph__Node__Data()
        self.node       = Schema__MGraph__Node      (node_data = self.node_data      ,
                                                     node_type = Schema__MGraph__Node)

    def test_init(self):                                                                            # Tests basic initialization and type checking
        assert type(self.node)     is Schema__MGraph__Node
        assert self.node.node_data == self.node_data

    def test_type_safety_validation(self):                                                          # Tests type safety validations
        error_message = "On Schema__MGraph__Node, invalid type for attribute 'node_data'. Expected '<class 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'>' but got '<class 'str'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Schema__MGraph__Node(node_data   = "not-a-node-config"                         ,        # Should be Schema__MGraph__Node__Config
                                 node_type   = Schema__MGraph__Node                        )