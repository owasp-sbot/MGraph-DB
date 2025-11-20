from unittest                                                        import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id     import is_obj_id
from mgraph_db.mgraph.models.Model__MGraph__Node                     import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                   import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data             import Schema__MGraph__Node__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id    import Safe_Id
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node       import Schema__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data import Schema__Mermaid__Node__Data
from mgraph_db.providers.mermaid.models.Model__Mermaid__Node         import Model__Mermaid__Node

class test_Model__Mermaid__Node(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.node_data = Schema__Mermaid__Node__Data()
        self.key = Safe_Id('test_key')
        self.node = Schema__Mermaid__Node(node_data  = self.node_data       ,
                                          node_type  = Schema__Mermaid__Node,
                                          key        = self.key             ,
                                          label      = "Test Label"         )
        self.model = Model__Mermaid__Node(data=self.node)

    def test_init(self):                                                            # Tests basic initialization
        assert type(self.model)         is Model__Mermaid__Node
        assert self.model.data          is self.node
        assert self.model.data.key      == self.key
        assert self.model.data.label    == "Test Label"

    def test_ensure_label_is_set_with_empty_label(self):                           # Tests label initialization when empty
        node = Schema__Mermaid__Node(node_data = self.node_data     ,
                                     node_type   = Schema__Mermaid__Node,
                                     key        = self.key              ,
                                     label      = ""                    )         # Empty label
        model = Model__Mermaid__Node(data=node)

        assert model.data.label == self.key                                        # Label should be set to key

    def test_ensure_label_is_set_with_none_label(self):                           # Tests label initialization when None
        node = Schema__Mermaid__Node(node_data = self.node_data     ,
                                     node_type   = Schema__Mermaid__Node,
                                     key        = self.key              ,
                                     label      = None                  )                                    # None label
        model = Model__Mermaid__Node(data=node)

        assert model.data.label == self.key                                       # Label should be set to key

    def test_existing_label_preserved(self):                                      # Tests that existing labels are not overwritten
        existing_label = "Existing Label"
        node = Schema__Mermaid__Node(node_data = self.node_data     ,
                                     node_type   = Schema__Mermaid__Node,
                                     key        = self.key              ,
                                     label      = existing_label        )
        model = Model__Mermaid__Node(data=node)

        assert model.data.label == existing_label                                       # Label should remain unchanged

    def test_inheritance_from_model_mgraph_node(self):                                  # Tests inheritance behavior
        assert isinstance(self.model, Model__MGraph__Node)                              # Verify that Model__Mermaid__Node inherits Model__MGraph__Node functionality
        assert is_obj_id(self.model.node_id)

    def test_mermaid_specific_implementations(self):                                    # Tests Mermaid-specific class implementations
        assert issubclass(Schema__Mermaid__Node, Schema__MGraph__Node)                  # Verify schema inheritance
        assert hasattr(Schema__Mermaid__Node(), 'key')
        assert hasattr(Schema__Mermaid__Node(), 'label')

        assert isinstance(self.node_data, Schema__Mermaid__Node__Data)              # Verify that the node uses Mermaid-specific config
        assert issubclass(Schema__Mermaid__Node__Data, Schema__MGraph__Node__Data)

        assert issubclass(Model__Mermaid__Node, Model__MGraph__Node)  is True                       # Verify model inheritance and implementation
        assert isinstance(self.model.data, Schema__Mermaid__Node)     is True
        assert type(self.model.data)                                  is Schema__Mermaid__Node      # Verify exact type match
        assert not type(self.model.data)                              is Schema__MGraph__Node       # Should be exact type match

        assert hasattr   (self.model.data      , 'key'  )                               # Test Mermaid-specific attributes
        assert hasattr   (self.model.data      , 'label')
        assert isinstance(self.model.data.key  , Safe_Id)
        assert isinstance(self.model.data.label, str    )

    def test_mermaid_config_specifics(self):                                      # Tests Mermaid-specific configuration
        # Create node config with Mermaid-specific settings
        node_data = Schema__Mermaid__Node__Data(markdown         = True,
                                                show_label       = False,
                                                wrap_with_quotes = True)

        # Create node with this config
        node = Schema__Mermaid__Node(node_data  = node_data             ,
                                     node_type   = Schema__Mermaid__Node,
                                     key        = Safe_Id('test_key')   ,
                                     label      = "Test Label"          )
        model = Model__Mermaid__Node(data=node)

        # Verify Mermaid-specific config options
        assert hasattr(model.data.node_data, 'markdown')
        assert hasattr(model.data.node_data, 'show_label')
        assert hasattr(model.data.node_data, 'wrap_with_quotes')
        assert model.data.node_data.markdown is True
        assert model.data.node_data.show_label is False
        assert model.data.node_data.wrap_with_quotes is True