import pytest
from io                                                                import StringIO
from unittest                                                          import TestCase
from unittest.mock                                                     import patch
from osbot_utils.utils.Misc                                            import str_md5, lower
from mgraph_db.mgraph.MGraph                                           import MGraph
from mgraph_db.mgraph.index.MGraph__Index__Values                      import MGraph__Index__Values, SIZE__VALUE_HASH
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value              import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Value__Index__Data import Schema__MGraph__Value__Index__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data        import Schema__MGraph__Node__Value__Data


class test_MGraph__Index__Values(TestCase):

    def setUp(self):
        self.mgraph       = MGraph()
        self.values_index = MGraph__Index__Values()

    def test__setUp(self):
        with self.values_index as _:
            assert type(_           ) is MGraph__Index__Values
            assert type(_.index_data) is Schema__MGraph__Value__Index__Data
            assert _.json()           == {  'enabled'    : True                   ,
                                            'index_data' : { 'hash_to_node'   : {},
                                                            'node_to_hash'    : {},
                                                            'values_by_type'  : {},
                                                            'type_by_value'   : {} }}

    # =========================================================================
    # Add Value Node Tests
    # =========================================================================

    def test_add_value_node(self):
        value                = "test_value"
        value_type           = type(value)
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value      = value     ,
                                                                 value_type = value_type)
        hash_str              = f"schema__mgraph__node__value::{value_type.__module__}.{value_type.__name__}::{value}"
        value_node_id         = value_node.node_id
        value_node_id_str     = str(value_node_id)

        with self.values_index as _:

            _.add_value_node(value_node)

            expected_hash        = _.calculate_hash(str, value, node_type=type(value_node))
            expected_hash_str    = str(expected_hash)
            expected_hash_type   = _.index_data.type_by_value[expected_hash]
            assert expected_hash == str_md5(hash_str)[:SIZE__VALUE_HASH]
            assert expected_hash == "3f2e519923"
            assert _.index_data.json() == { 'hash_to_node'  : { expected_hash_str : value_node_id_str  },
                                            'node_to_hash'  : { value_node_id_str : expected_hash_str  },
                                            'type_by_value' : { expected_hash_str : 'builtins.str'     },
                                            'values_by_type': { 'builtins.str'    : [expected_hash_str]}}

            assert value_type           is str
            assert value_node.node_id   in _.index_data.node_to_hash
            assert expected_hash        in _.index_data.hash_to_node
            assert str                  in _.index_data.values_by_type
            assert expected_hash        in _.index_data.values_by_type[str]
            assert expected_hash        in _.index_data.type_by_value
            assert expected_hash_type   is str

    def test_add_value_node__multiple_types(self):
        def create_value_node(value):
            node = Schema__MGraph__Node__Value()
            node.node_data = Schema__MGraph__Node__Value__Data(value      = str (value),
                                                               value_type = type(value))
            return node

        with self.values_index as _:
            int_value         = 42
            float_value       = 3.14
            bool_value        = True
            int_node          = create_value_node(int_value  )
            float_node        = create_value_node(float_value)
            bool_node         = create_value_node(bool_value )
            int_node_id       = int_node.node_id
            float_node_id     = float_node.node_id
            bool_node_id      = bool_node.node_id

            int_node_id_str   = str(int_node_id)
            float_node_id_str = str(float_node_id)
            bool_node_id_str  = str(bool_node_id)

            node_type         = Schema__MGraph__Node__Value
            node_type_name    = node_type.__name__
            int_hash_str      = lower(f"{node_type_name}::{int.__module__}.{int.__name__}::{int_value}"       )
            float_hash_str    = lower(f"{node_type_name}::{float.__module__}.{float.__name__}::{float_value}" )
            bool_hash_str     = lower(f"{node_type_name}::{bool.__module__}.{bool.__name__}::{bool_value}"    )

            _.add_value_node(int_node  )
            _.add_value_node(float_node)
            _.add_value_node(bool_node )

            assert type(int_node  ) is Schema__MGraph__Node__Value
            assert type(float_node) is Schema__MGraph__Node__Value
            assert type(bool_node ) is Schema__MGraph__Node__Value
            assert int              in _.index_data.values_by_type
            assert float            in _.index_data.values_by_type
            assert bool             in _.index_data.values_by_type
            assert int_hash_str     == 'schema__mgraph__node__value::builtins.int::42'
            assert float_hash_str   == 'schema__mgraph__node__value::builtins.float::3.14'
            assert bool_hash_str    == 'schema__mgraph__node__value::builtins.bool::true'
            assert 'f8bb59eae6'     == _.calculate_hash(int  , int_value   , node_type=node_type)
            assert '12b2368328'     == _.calculate_hash(float, float_value , node_type=node_type)
            assert '62bb187439'     == _.calculate_hash(bool , bool_value  , node_type=node_type)
            assert 'f8bb59eae6'     == str_md5(int_hash_str  )[:SIZE__VALUE_HASH]
            assert '12b2368328'     == str_md5(float_hash_str)[:SIZE__VALUE_HASH]
            assert '62bb187439'     == str_md5(bool_hash_str )[:SIZE__VALUE_HASH]

            assert _.index_data.json() == { 'hash_to_node' : { '62bb187439'       : bool_node_id_str  ,
                                                               'f8bb59eae6'       : int_node_id_str   ,
                                                               '12b2368328'       : float_node_id_str },
                                            'node_to_hash'  : { bool_node_id_str  : '62bb187439'      ,
                                                                float_node_id_str : '12b2368328'      ,
                                                                int_node_id_str   : 'f8bb59eae6'      },
                                            'type_by_value' : { '62bb187439'      : 'builtins.bool'   ,
                                                                'f8bb59eae6'      : 'builtins.int'    ,
                                                                '12b2368328'      : 'builtins.float'  },
                                            'values_by_type': { 'builtins.float'  : ['12b2368328'     ],
                                                                'builtins.bool'   : ['62bb187439'     ],
                                                                'builtins.int'    : ['f8bb59eae6'     ]}}

    def test_add_value_node__special_characters(self):
        value = "test::value::with::colons"
        value_node = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value=value, value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)
            expected_hash = _.calculate_hash(str, value, node_type=type(value_node))

            assert expected_hash in _.index_data.hash_to_node
            assert value_node.node_id in _.index_data.node_to_hash

    def test_add_value_node__duplicate(self):
        value_node_1 = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value= "test_value",value_type = str)

        value_node_2 = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value= "test_value", value_type = str)

        assert value_node_1.node_data.json() == {'key':'', 'value': 'test_value', 'value_type': 'builtins.str'}

        with self.values_index as _:
            _.add_value_node(value_node_1)
            assert value_node_1.node_data.json() == {'key':'', 'value': 'test_value', 'value_type': 'builtins.str'}
            with pytest.raises(ValueError, match=f"Value with hash 3f2e519923 already exists"):
                _.add_value_node(value_node_2)

    def test_add_value_node__invalid_node_data(self):
        with self.values_index as _:
            class CustomNode(Schema__MGraph__Node__Value):
                pass

            custom_node           = CustomNode()
            custom_node.node_data = None

            with pytest.raises(ValueError, match="not a subclass"):
                _.add_value_node(custom_node)

    # =========================================================================
    # Remove Value Node Tests
    # =========================================================================

    def test_remove_value_node(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= "test_value", value_type = str)
        value_node_id        = value_node.node_id
        value_node_id_str    = str(value_node_id)
        self.mgraph.edit().add_node(value_node)

        with self.values_index as _:
            _.add_value_node(value_node)
            hash_value = _.calculate_hash(str, "test_value", node_type=type(value_node))

            assert value_node.node_id in _.index_data.node_to_hash
            assert hash_value in _.index_data.hash_to_node
            assert hash_value in _.index_data.values_by_type[str]
            assert hash_value in _.index_data.type_by_value

            assert _.index_data.json() == { 'hash_to_node'  : {'3f2e519923'     : value_node_id_str },
                                            'node_to_hash'  : {value_node_id_str: '3f2e519923'      },
                                            'type_by_value' : {'3f2e519923'     : 'builtins.str'    },
                                            'values_by_type': { 'builtins.str'  : ['3f2e519923'    ]}}

            _.remove_value_node(value_node)
            assert _.index_data.json() == { 'hash_to_node'  : {},
                                            'node_to_hash'  : {},
                                            'type_by_value' : {},
                                            'values_by_type': {}}

            assert value_node.node_id not in _.index_data.node_to_hash
            assert hash_value         not in _.index_data.hash_to_node
            assert hash_value         not in _.index_data.type_by_value

    def test_remove_value_node__not_in_index(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="not_added", value_type=str)

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    def test_remove_value_node__type_not_in_values_by_type(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="orphan", value_type=str)

            _.add_value_node(value_node)
            del _.index_data.values_by_type[str]                                # Remove type manually

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    def test_remove_value_node__hash_not_in_type_by_value(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="orphan2", value_type=str)

            _.add_value_node(value_node)
            hash_value = _.index_data.node_to_hash[value_node.node_id]
            del _.index_data.type_by_value[hash_value]                          # Remove hash manually

            _.remove_value_node(value_node)                                     # Should not crash

            assert True

    # =========================================================================
    # Calculate Hash Tests
    # =========================================================================

    def test_calculate_hash(self):
        with self.values_index as _:
            hash_1 = _.calculate_hash(str, "test_value")
            hash_2 = _.calculate_hash(int, 42          )
            hash_3 = _.calculate_hash(str, "test_value")

            assert hash_1 == str_md5(f"{str.__module__}.{str.__name__}::{"test_value"}")[:SIZE__VALUE_HASH]
            assert hash_2 == str_md5(f"{int.__module__}.{int.__name__}::{"42"}"        )[:SIZE__VALUE_HASH]
            assert hash_3 == str_md5(f"{str.__module__}.{str.__name__}::{"test_value"}")[:SIZE__VALUE_HASH]
            assert hash_1 == "c056cc97b9"
            assert hash_2 == "d77fb78183"
            assert hash_1 == hash_3
            assert hash_1 != hash_2

    def test_calculate_hash__with_key(self):
        with self.values_index as _:
            hash_without_key = _.calculate_hash(str, "value")
            hash_with_key    = _.calculate_hash(str, "value", key="my_key")

            assert hash_without_key != hash_with_key                            # Key should change hash

    def test_calculate_hash__none_value_type(self):
        with self.values_index as _:
            with pytest.raises(ValueError, match="Parameter 'value_type' is not optional but got None"):
                _.calculate_hash(None, "value")

    def test_calculate_hash__with_node_type(self):
        with self.values_index as _:
            hash_without_node_type = _.calculate_hash(str, "value")
            hash_with_node_type    = _.calculate_hash(str, "value", node_type=Schema__MGraph__Node__Value)

            assert hash_without_node_type != hash_with_node_type                # node_type should change hash

    def test_calculate_hash__with_all_params(self):
        with self.values_index as _:
            result = _.calculate_hash(value_type = str                       ,
                                      value      = "test"                    ,
                                      key        = "my_key"                  ,
                                      node_type  = Schema__MGraph__Node__Value)

            assert len(result) == SIZE__VALUE_HASH

    # =========================================================================
    # Get Methods Tests
    # =========================================================================

    def test_get_node_id_by_hash(self):
        value                = "test_value"
        value_node           = Schema__MGraph__Node__Value()
        value_node_id        = value_node.node_id
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= value,value_type = str)
        with self.values_index as _:
            _.add_value_node(value_node)
            hash_value         = _.calculate_hash(str, "test_value", node_type=type(value_node))
            retrieved_node_id  = _.get_node_id_by_hash(hash_value)
            assert retrieved_node_id                     == value_node_id
            assert _.get_node_id_by_hash("non_existent") is None

    def test_get_node_id_by_value(self):
        value                = "test_value"
        value_node           = Schema__MGraph__Node__Value()
        value_node_id        = value_node.node_id
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= value,value_type = str)

        with self.values_index as _:
            _.add_value_node(value_node)

            retrieved_node_id = _.get_node_id_by_value(str, value, node_type=type(value_node))
            assert retrieved_node_id                           == value_node_id
            assert _.get_node_id_by_value(str, "non_existent") is None
            assert _.get_node_id_by_value(int, "test_value"  ) is None

    def test_get_node_id_by_value__with_key(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="keyed_value", value_type=str, key="my_key")

            _.add_value_node(value_node)

            result = _.get_node_id_by_value(str, "keyed_value", key="my_key", node_type=Schema__MGraph__Node__Value)

            assert result == value_node.node_id

    def test_get_node_id_by_value__with_default_node_type(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="default_type", value_type=str)

            _.add_value_node(value_node)

            result = _.get_node_id_by_value(str, "default_type", node_type=Schema__MGraph__Node__Value)

            assert result == value_node.node_id

    # =========================================================================
    # Raw Data Accessor Tests
    # =========================================================================

    def test_hash_to_node__accessor(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="accessor_test", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)
            hash_value = _.calculate_hash(str, "accessor_test", node_type=type(value_node))

            result = _.hash_to_node()

            assert hash_value in result
            assert result[hash_value] == value_node.node_id

    def test_node_to_hash__accessor(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="accessor_test", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)

            result = _.node_to_hash()

            assert value_node.node_id in result

    def test_values_by_type__accessor(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="type_test", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)

            result = _.values_by_type()

            assert str in result

    def test_type_by_value__accessor(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="type_test", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)
            hash_value = _.calculate_hash(str, "type_test", node_type=type(value_node))

            result = _.type_by_value()

            assert hash_value in result
            assert result[hash_value] is str

    # =========================================================================
    # Query Method Tests
    # =========================================================================

    def test_has_hash(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="has_hash_test", value_type=str)

        with self.values_index as _:
            hash_value = _.calculate_hash(str, "has_hash_test", node_type=type(value_node))

            assert _.has_hash(hash_value) is False

            _.add_value_node(value_node)

            assert _.has_hash(hash_value)     is True
            assert _.has_hash("nonexistent")  is False

    def test_has_node(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="has_node_test", value_type=str)
        other_node           = Schema__MGraph__Node__Value()
        other_node.node_data = Schema__MGraph__Node__Value__Data(value="other", value_type=str)

        with self.values_index as _:
            assert _.has_node(value_node.node_id) is False

            _.add_value_node(value_node)

            assert _.has_node(value_node.node_id) is True
            assert _.has_node(other_node.node_id) is False

    def test_get_hash_for_node(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="get_hash_test", value_type=str)
        other_node           = Schema__MGraph__Node__Value()
        other_node.node_data = Schema__MGraph__Node__Value__Data(value="other", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)
            expected_hash = _.calculate_hash(str, "get_hash_test", node_type=type(value_node))

            assert _.get_hash_for_node(value_node.node_id) == expected_hash
            assert _.get_hash_for_node(other_node.node_id) is None

    def test_get_hashes_by_type(self):
        value_node_1           = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value="str_value_1", value_type=str)
        value_node_2           = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value="str_value_2", value_type=str)
        value_node_3           = Schema__MGraph__Node__Value()
        value_node_3.node_data = Schema__MGraph__Node__Value__Data(value="42", value_type=int)

        with self.values_index as _:
            _.add_value_node(value_node_1)
            _.add_value_node(value_node_2)
            _.add_value_node(value_node_3)

            str_hashes = _.get_hashes_by_type(str)
            int_hashes = _.get_hashes_by_type(int)

            assert len(str_hashes) == 2
            assert len(int_hashes) == 1
            assert _.get_hashes_by_type(float) == set()

    # def test_get_type_for_hash(self):
    #     value_node           = Schema__MGraph__Node__Value()
    #     value_node.node_data = Schema__MGraph__Node__Value__Data(value="type_for_hash", value_type=str)
    #
    #     with self.values_index as _:
    #         _.add_value_node(value_node)
    #         hash_value = _.calculate_hash(str, "type_for_hash", node_type=type(value_node))
    #
    #         assert _.get_type_for_hash(hash_value)     is str
    #         assert _.get_type_for_hash("nonexistent")  is None

    def test_get_all_hashes(self):
        value_node_1           = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value="value_1", value_type=str)
        value_node_2           = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value="value_2", value_type=str)

        with self.values_index as _:
            assert _.get_all_hashes() == set()

            _.add_value_node(value_node_1)
            _.add_value_node(value_node_2)

            assert len(_.get_all_hashes()) == 2

    def test_get_all_types(self):
        value_node_1           = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value="str_val", value_type=str)
        value_node_2           = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value="42", value_type=int)

        with self.values_index as _:
            assert _.get_all_types() == set()

            _.add_value_node(value_node_1)
            _.add_value_node(value_node_2)

            result = _.get_all_types()
            assert str in result
            assert int in result
            assert len(result) == 2

    # =========================================================================
    # Count Method Tests
    # =========================================================================

    def test_count_values(self):
        value_node_1           = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value="count_1", value_type=str)
        value_node_2           = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value="count_2", value_type=str)

        with self.values_index as _:
            assert _.count_values() == 0

            _.add_value_node(value_node_1)
            assert _.count_values() == 1

            _.add_value_node(value_node_2)
            assert _.count_values() == 2

    def test_count_by_type(self):
        value_node_1           = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value="str_1", value_type=str)
        value_node_2           = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value="str_2", value_type=str)
        value_node_3           = Schema__MGraph__Node__Value()
        value_node_3.node_data = Schema__MGraph__Node__Value__Data(value="42", value_type=int)

        with self.values_index as _:
            assert _.count_by_type(str) == 0
            assert _.count_by_type(int) == 0

            _.add_value_node(value_node_1)
            _.add_value_node(value_node_2)
            _.add_value_node(value_node_3)

            assert _.count_by_type(str)   == 2
            assert _.count_by_type(int)   == 1
            assert _.count_by_type(float) == 0

    # =========================================================================
    # Enabled/Disabled Tests
    # =========================================================================

    def test_add_value_node__disabled(self):                                    # Test add does nothing when disabled
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="test_value", value_type=str)

        with self.values_index as _:
            _.enabled = False
            _.add_value_node(value_node)

            assert _.count_values()   == 0                                      # Nothing indexed
            assert _.hash_to_node()   == {}
            assert _.node_to_hash()   == {}

    def test_remove_value_node__disabled(self):                                 # Test remove does nothing when disabled
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value="test_value", value_type=str)

        with self.values_index as _:
            _.add_value_node(value_node)                                        # Add while enabled
            assert _.has_node(value_node.node_id) is True

            _.enabled = False
            _.remove_value_node(value_node)                                     # Remove while disabled

            assert _.has_node(value_node.node_id) is True                       # Still there

    # =========================================================================
    # Print Method Tests
    # =========================================================================

    def test_print__values_index_data(self):
        with self.values_index as _:
            value_node           = Schema__MGraph__Node__Value()
            value_node.node_data = Schema__MGraph__Node__Value__Data(value="print_test", value_type=str)

            _.add_value_node(value_node)

            with patch('sys.stdout', new_callable=StringIO):                    # Capture stdout
                _.print__values_index_data()

            assert True                                                         # Method executed without error