from unittest                                                           import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id


class test_Schema__Mermaid__Edge__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.edge_id        = Obj_Id()
        self.from_node_type = Schema__Mermaid__Node
        self.to_node_type   = Schema__Mermaid__Node
        self.edge_config    = Schema__Mermaid__Edge__Config()

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.edge_config)           is Schema__Mermaid__Edge__Config
        assert self.edge_id         == self.edge_id



