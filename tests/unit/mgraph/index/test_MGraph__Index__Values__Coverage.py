import pytest
from io                                                             import StringIO
from unittest                                                       import TestCase
from unittest.mock                                                  import patch
from mgraph_db.mgraph.index.MGraph__Index__Values                   import MGraph__Index__Values, SIZE__VALUE_HASH
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data


class test_MGraph__Index__Values__Coverage(TestCase):           # Additional tests targeting uncovered code paths in MGraph__Index__Values

    def setUp(self):
        self.values_index = MGraph__Index__Values()

    # =========================================================================
    # Calculate Hash Edge Cases
    # =========================================================================

    def test_calculate_hash__with_key(self):                                    # Test calculate_hash with key parameter
        with self.values_index as _:
            hash_without_key = _.calculate_hash(str, "value")
            hash_with_key    = _.calculate_hash(str, "value", key="my_key")

            assert hash_without_key != hash_with_key                            # Key should change hash

    def test_calculate_hash__none_value_type(self):                             # Test calculate_hash with None value_type
        with self.values_index as _:
            with pytest.raises(ValueError, match="Parameter 'value_type' is not optional but got None"):
                _.calculate_hash(None, "value")

    def test_calculate_hash__with_node_type(self):                              # Test calculate_hash with node_type parameter
        with self.values_index as _:
            hash_without_node_type = _.calculate_hash(str, "value")
            hash_with_node_type    = _.calculate_hash(str, "value", node_type=Schema__MGraph__Node__Value)

            assert hash_without_node_type != hash_with_node_type                # node_type should change hash

    def test_calculate_hash__with_all_params(self):                             # Test with all parameters
        with self.values_index as _:
            result = _.calculate_hash(value_type = str                       ,
                                      value      = "test"                    ,
                                      key        = "my_key"                  ,
                                      node_type  = Schema__MGraph__Node__Value)

            assert len(result) == SIZE__VALUE_HASH

    # =========================================================================
    # Remove Value Node Edge Cases
    # =========================================================================

    def test_remove_value_node__not_in_index(self):                             # Test removing node not in index
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="not_added", value_type=str)

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    def test_remove_value_node__type_not_in_values_by_type(self):               # Test when type already removed
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="orphan", value_type=str)

            _.add_value_node(value_node)
            del _.index_data.values_by_type[str]                                # Remove type manually

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    def test_remove_value_node__hash_not_in_type_by_value(self):                # Test when hash already removed from type_by_value
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="orphan2", value_type=str)

            _.add_value_node(value_node)
            hash_value = _.index_data.node_to_hash[value_node.node_id]
            del _.index_data.type_by_value[hash_value]                          # Remove hash manually

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    # =========================================================================
    # Add Value Node Edge Cases
    # =========================================================================

    def test_add_value_node__invalid_node_data(self):                           # Test with invalid node data
        with self.values_index as _:
            class CustomNode(Schema__MGraph__Node__Value):
                pass

            custom_node           = CustomNode()
            custom_node.node_data = None                                        # Invalid - not Schema__MGraph__Node__Value__Data

            with pytest.raises(ValueError, match="not a subclass"):
                _.add_value_node(custom_node)

    # =========================================================================
    # Print Method
    # =========================================================================

    def test_print__values_index_data(self):                                    # Test print method
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="print_test", value_type=str)

            _.add_value_node(value_node)

            with patch('sys.stdout', new_callable=StringIO):                    # Capture stdout
                _.print__values_index_data()

            assert True                                                         # Method executed without error

    # =========================================================================
    # Get Methods Edge Cases
    # =========================================================================

    def test_get_node_id_by_value__with_key(self):                              # Test get with key parameter
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="keyed_value", value_type=str, key="my_key")

            _.add_value_node(value_node)

            result = _.get_node_id_by_value(str, "keyed_value", key="my_key", node_type=Schema__MGraph__Node__Value)

            assert result == value_node.node_id

    def test_get_node_id_by_value__with_default_node_type(self):                # Test get with default node_type
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="default_type", value_type=str)

            _.add_value_node(value_node)

            result = _.get_node_id_by_value(str, "default_type", node_type=Schema__MGraph__Node__Value)

            assert result == value_node.node_id