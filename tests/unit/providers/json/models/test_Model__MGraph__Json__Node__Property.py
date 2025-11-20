from unittest                                                                       import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data    import Schema__MGraph__Json__Node__Property__Data
from osbot_utils.utils.Objects                                                      import type_full_name
from osbot_utils.testing.__                                                         import __
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Property            import Model__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property          import Schema__MGraph__Json__Node__Property

class test_Model__MGraph__Json__Node__Property(TestCase):
    @classmethod

    def test_init(self):                                                                            # Test base JSON property node model initialization
        with Model__MGraph__Json__Node__Property(data=Schema__MGraph__Json__Node__Property()) as _:  # Create base JSON property node model
            assert _.obj() == __(data =__(node_data = __(name = ''),
                                         node_id    = _.node_id,
                                         node_type  = type_full_name(Schema__MGraph__Json__Node__Property)))

    def test_property_node_creation(self):                                                          # Test creating a property node model
        # Create schema node with property data
        node_data = Schema__MGraph__Json__Node__Property__Data(name='test_property')                # Create schema node with property data
        schema_node = Schema__MGraph__Json__Node__Property(node_data=node_data)                     # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Property(data=schema_node)                          # Create model node

        # Verify properties
        assert model_node.name == "test_property"

    def test_set_property_name(self):                                                               # Test changing property name
        # Create schema node with initial name
        node_data = Schema__MGraph__Json__Node__Property__Data(name='original_name')                # Create schema node with initial name
        schema_node = Schema__MGraph__Json__Node__Property(node_data=node_data)                     # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Property(data=schema_node)                          # Create model node

        # Change name
        model_node.name = "new_name"                                                                # Change property name

        # Verify updated properties
        assert model_node.name == "new_name"
        assert model_node.data.node_data.name == "new_name"