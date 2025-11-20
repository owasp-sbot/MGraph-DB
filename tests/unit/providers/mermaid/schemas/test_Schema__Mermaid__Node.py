from unittest                                                        import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data import Schema__Mermaid__Node__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id    import Safe_Id
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node       import Schema__Mermaid__Node

class test_Schema__Mermaid__Node(TestCase):

    def setUp(self):                                                                     # Initialize test data
        self.node_data = Schema__Mermaid__Node__Data    ()
        self.node        = Schema__Mermaid__Node        (node_data     = self.node_data       ,
                                                         node_type       = Schema__Mermaid__Node  ,
                                                         key             = Safe_Id("node_1")      ,
                                                         label           = "Test Node"            )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.node)             is Schema__Mermaid__Node
        assert self.node.node_data         == self.node_data
        assert type(self.node.key)        is Safe_Id
        assert str(self.node.key)         == "node_1"
        assert self.node.label            == "Test Node"

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node(node_data = self.node_data ,
                                  node_type = 123            ,            # invalid type for note type
                                  key       = 'an-key'       ,
                                  label     = "Test Node"    )
        assert "Invalid type for attribute 'node_type'" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node(node_data = self.node_data          ,
                                  node_type   = Schema__Mermaid__Node ,
                                  key         = Safe_Id("node_1")     ,
                                  label       = 123                   )            # Invalid type for label
        assert "Invalid type for attribute 'label'" in str(context.exception)


    def test_json_serialization(self):                                              # Tests JSON serialization and deserialization
        json_data = self.node.json()

        # Verify JSON structure
        assert 'key'         in json_data
        assert 'label'       in json_data
        assert 'node_data' in json_data

        # Test deserialization
        restored = Schema__Mermaid__Node.from_json(json_data)
        assert str(restored.key)        == str(self.node.key)
        assert restored.label           == self.node.label
        assert restored.node_type       == self.node.node_type


