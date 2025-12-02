import re
import pytest
from unittest                                                     import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data          import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.identifiers.Node_Path               import Node_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id


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

    def test_node_with_path(self):                                                                  # Test node creation with path
        with Schema__MGraph__Node( node_id   = Node_Id()                    ,
                                   node_type = Schema__MGraph__Node         ,
                                   node_data = Schema__MGraph__Node__Data() ,
                                   node_path = Node_Path("html.body.div")   ) as _:
            assert _.node_path      == Node_Path("html.body.div")
            assert str(_.node_path) == "html.body.div"

    def test_node_without_path(self):                                                               # Test node creation without path (backward compatibility)
        with Schema__MGraph__Node( node_id   = Node_Id()                    ,
                                   node_type = Schema__MGraph__Node         ,
                                   node_data = Schema__MGraph__Node__Data() ) as _:
            assert _.node_path is None

    def test_node_path_default_none(self):                                                          # Test that node_path defaults to None
        with Schema__MGraph__Node( node_id   = Node_Id()                    ,
                                   node_type = Schema__MGraph__Node         ,
                                   node_data = Schema__MGraph__Node__Data() ) as _:
            assert _.node_path is None

    def test_node_serialization_roundtrip_with_path(self):                                          # Test that path survives serialization
        with Schema__MGraph__Node( node_id   = Node_Id()                    ,
                                   node_type = Schema__MGraph__Node         ,
                                   node_data = Schema__MGraph__Node__Data() ,
                                   node_path = Node_Path("test.path[1]")    ) as _:
            json_data = _.json()
            restored  = Schema__MGraph__Node.from_json(json_data)

            assert restored.node_path      == _.node_path
            assert str(restored.node_path) == "test.path[1]"

    def test_node_serialization_roundtrip_without_path(self):                                       # Test that nodes without paths serialize correctly
        with Schema__MGraph__Node( node_id   = Node_Id()                    ,
                                   node_type = Schema__MGraph__Node         ,
                                   node_data = Schema__MGraph__Node__Data() ) as _:
            json_data = _.json()
            restored  = Schema__MGraph__Node.from_json(json_data)

            assert restored.node_path is None