import re
import pytest
from unittest                                                                   import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data   import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.utils.Objects                                                  import type_full_name
from osbot_utils.testing.__                                                     import __
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value           import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value         import Schema__MGraph__Json__Node__Value


class test_Model__MGraph__Json__Node__Value(TestCase):
    def test_init(self):                                                                            # Test base JSON value node model initialization
        with Model__MGraph__Json__Node__Value(data=Schema__MGraph__Json__Node__Value()) as _:        # Create base JSON value node model
            assert _.obj() == __(data = __(node_data = __(value      = None ,
                                                          value_type = None),
                                           node_id   = _.data.node_id,
                                           node_type = type_full_name(Schema__MGraph__Json__Node__Value)))

    def test_value_node_creation(self):                                                             # Test creating a value node model
        node_data   = Schema__MGraph__Json__Node__Value__Data(value="hello", value_type=str)        # Create schema node with value data
        schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)                        # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Value(data=schema_node)                             # Create model node

        # Verify properties
        assert model_node.value == "hello"
        assert model_node.value_type == str
        assert model_node.is_primitive() is True

    def test_value_and_type_updates(self):                                                          # Create schema node with initial value
        node_data   = Schema__MGraph__Json__Node__Value__Data(value=42, value_type=int)
        schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)
        model_node  = Model__MGraph__Json__Node__Value(data=schema_node)

        assert model_node.value == 42                                                               # Verify initial state
        assert model_node.value_type == int


        model_node.value = "new value"                                                              # Update with different types and verify type is automatically updated
        assert model_node.value      == "new value"
        assert model_node.value_type == str

        model_node.value = 3.14
        assert model_node.value      == 3.14
        assert model_node.value_type == float

        model_node.value = True
        assert model_node.value      == True
        assert model_node.value_type == bool

        error_message = "On Schema__MGraph__Json__Node__Value__Data, can't be set to None, to a variable that is already set. Invalid type for attribute 'value'. Expected 'typing.Any' but got '<class 'NoneType'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            model_node.value        = None

    def test_primitive_check(self):                                                                 # Test primitive type detection
        # Test various primitive types
        test_cases = [(42       , int, True        ),
                      (3.14     , float, True      ),
                      ("hello"  , str, True        ),
                      (True     , bool, True       ),
                      (None     , type(None), True )]

        for value, value_type, expected_primitive in test_cases:                                    # Iterate through test cases
            node_data = Schema__MGraph__Json__Node__Value__Data(value=value, value_type=value_type) # Create node data
            schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)                    # Create schema node
            model_node = Model__MGraph__Json__Node__Value(data=schema_node)                         # Create model node

            assert model_node.is_primitive() is expected_primitive

