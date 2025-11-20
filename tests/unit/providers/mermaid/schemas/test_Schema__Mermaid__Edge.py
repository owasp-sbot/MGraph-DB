from unittest                                                            import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id         import Obj_Id


class test_Schema__Mermaid__Edge(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.edge_config = Schema__Mermaid__Edge__Config()

        self.edge = Schema__Mermaid__Edge(edge_config  = self.edge_config         ,
                                          edge_type    = Schema__Mermaid__Edge    ,
                                          from_node_id = Obj_Id()                 ,
                                          to_node_id   = Obj_Id()                 ,
                                          label        = "Test Edge"              )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.edge)             is Schema__Mermaid__Edge
        assert self.edge.edge_config       == self.edge_config
        assert self.edge.label             == "Test Edge"

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Edge(edge_config  = self.edge_config      ,
                                  edge_type    = Schema__Mermaid__Edge ,
                                  from_node_id = Obj_Id()              ,
                                  to_node_id   = Obj_Id()              ,
                                  label        = 123                   ) # Invalid type for label
        assert "Invalid type for attribute 'label'" in str(context.exception)

    def test_json_serialization(self):                                              # Tests JSON serialization and deserialization
        json_data = self.edge.json()

        # Verify JSON structure
        assert 'label'        in json_data
        assert 'edge_config'  in json_data
        assert 'from_node_id' in json_data
        assert 'to_node_id'   in json_data

        # Test deserialization
        restored = Schema__Mermaid__Edge.from_json(json_data)
        assert restored.label       == self.edge.label
        assert restored.edge_type   == self.edge.edge_type
        assert restored.edge_id == self.edge.edge_id