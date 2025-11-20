import pytest
from unittest                                                       import TestCase
from osbot_utils.utils.Misc                                         import str_md5, lower
from mgraph_db.mgraph.MGraph                                        import MGraph
from mgraph_db.mgraph.actions.MGraph__Index__Values                 import MGraph__Index__Values, SIZE__VALUE_HASH
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Value__Index__Data    import Schema__MGraph__Value__Index__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data

class test_MGraph__Index__Values(TestCase):

    def setUp(self):
        self.mgraph      = MGraph()
        self.value_index = MGraph__Index__Values()

    # def tearDown(self):
    #     self.value_index.print__values_index_data()

    def test__setUp(self):
        with self.value_index as _:
            assert type(_           ) is MGraph__Index__Values
            assert type(_.index_data) is Schema__MGraph__Value__Index__Data
            assert _.json()           == { 'index_data' : { 'hash_to_node'   : {},
                                                            'node_to_hash'    : {},
                                                            'values_by_type'  : {},
                                                            'type_by_value'   : {} }}

    def test_add_value_node(self):
        value                = "test_value"
        value_type           = type(value)
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value      = value     ,
                                                                 value_type = value_type)
        hash_str              = f"schema__mgraph__node__value::{value_type.__module__}.{value_type.__name__}::{value}"
        value_node_id         = value_node.node_id
        with self.value_index as _:

            _.add_value_node(value_node)

            expected_hash        = _.calculate_hash(str, value, node_type=type(value_node))
            expected_hash_type   = _.index_data.type_by_value[expected_hash]
            assert expected_hash == str_md5(hash_str)[:SIZE__VALUE_HASH]
            assert expected_hash == "3f2e519923"
            assert _.index_data.json() == { 'hash_to_node'  : { expected_hash : value_node_id    },
                                            'node_to_hash'  : { value_node_id : expected_hash    },
                                            'type_by_value' : { expected_hash : 'builtins.str'   },
                                            'values_by_type': { 'builtins.str':  {expected_hash}}}

            assert value_type           is str
            assert value_node.node_id   in _.index_data.node_to_hash
            assert expected_hash        in _.index_data.hash_to_node
            assert str                  in _.index_data.values_by_type
            assert expected_hash        in _.index_data.values_by_type[str]
            assert expected_hash        in _.index_data.type_by_value
            assert expected_hash_type   is str

    def test_add_value_node__multiple_types(self):                              # Test different value types
        def create_value_node(value):
            node = Schema__MGraph__Node__Value()
            node.node_data = Schema__MGraph__Node__Value__Data(value      = str (value),
                                                               value_type = type(value))
            return node

        with self.value_index as _:
            int_value      = 42
            float_value    = 3.14
            bool_value     = True
            int_node       = create_value_node(int_value  )
            float_node     = create_value_node(float_value)
            bool_node      = create_value_node(bool_value )
            int_node_id    = int_node.node_id
            float_node_id  = float_node.node_id
            bool_node_id   = bool_node.node_id
            node_type      = Schema__MGraph__Node__Value
            node_type_name = node_type.__name__
            int_hash_str   = lower(f"{node_type_name}::{int.__module__}.{int.__name__}::{int_value}"       )
            float_hash_str = lower(f"{node_type_name}::{float.__module__}.{float.__name__}::{float_value}" )
            bool_hash_str  = lower(f"{node_type_name}::{bool.__module__}.{bool.__name__}::{bool_value}"    )

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

            assert _.index_data.json() == { 'hash_to_node' : { '62bb187439'     : bool_node_id    ,
                                                               'f8bb59eae6'     : int_node_id     ,
                                                               '12b2368328'     : float_node_id   },
                                            'node_to_hash'  : { bool_node_id    : '62bb187439'    ,
                                                                float_node_id   : '12b2368328'    ,
                                                                int_node_id     : 'f8bb59eae6'    },
                                            'type_by_value' : { '62bb187439'    : 'builtins.bool' ,
                                                                'f8bb59eae6'    : 'builtins.int'  ,
                                                                '12b2368328'    : 'builtins.float'},
                                            'values_by_type': { 'builtins.float': {'12b2368328'   },
                                                                'builtins.bool' : {'62bb187439'   },
                                                                'builtins.int'  : {'f8bb59eae6'   }}}

    def test_add_value_node__special_characters(self):                           # Test special character handling
        value = "test::value::with::colons"
        value_node = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value=value, value_type=str)

        with self.value_index as _:
            _.add_value_node(value_node)
            expected_hash = _.calculate_hash(str, value, node_type=type(value_node))

            assert expected_hash in _.index_data.hash_to_node
            assert value_node.node_id in _.index_data.node_to_hash

    def test_add_duplicate_value(self):
        value_node_1 = Schema__MGraph__Node__Value()
        value_node_1.node_data = Schema__MGraph__Node__Value__Data(value= "test_value",value_type = str)

        value_node_2 = Schema__MGraph__Node__Value()
        value_node_2.node_data = Schema__MGraph__Node__Value__Data(value= "test_value", value_type = str)

        assert value_node_1.node_data.json() == {'key':'', 'value': 'test_value', 'value_type': 'builtins.str'}

        with self.value_index as _:
            _.add_value_node(value_node_1)
            assert value_node_1.node_data.json() == {'key':'', 'value': 'test_value', 'value_type': 'builtins.str'}
            with pytest.raises(ValueError, match=f"Value with hash 3f2e519923 already exists"):
                _.add_value_node(value_node_2)

    def test_get_node_id_by_hash(self):
        value                = "test_value"
        value_node           = Schema__MGraph__Node__Value()
        value_node_id        = value_node.node_id
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= value,value_type = str)
        with self.value_index as _:
            _.add_value_node(value_node)
            hash_value         = _.calculate_hash(str, "test_value", node_type=type(value_node))
            retrieved_node_id  = _.get_node_id_by_hash(hash_value)
            assert retrieved_node_id                     == value_node_id
            assert _.get_node_id_by_hash("non_existent") is None                    # Test non-existent hash

    def test_get_node_id_by_value(self):
        value                = "test_value"
        value_node           = Schema__MGraph__Node__Value()
        value_node_id        = value_node.node_id
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= value,value_type = str)

        with self.value_index as _:
            _.add_value_node(value_node)

            retrieved_node_id = _.get_node_id_by_value(str, value, node_type=type(value_node))
            assert retrieved_node_id                           == value_node_id
            assert _.get_node_id_by_value(str, "non_existent") is None              # Test non-existent value
            assert _.get_node_id_by_value(int, "test_value"  ) is None

    def test_remove_value_node(self):
        value_node           = Schema__MGraph__Node__Value()
        value_node.node_data = Schema__MGraph__Node__Value__Data(value= "test_value", value_type = str)
        value_node_id        = value_node.node_id
        self.mgraph.edit().add_node(value_node)

        with self.value_index as _:
            _.add_value_node(value_node)
            hash_value = _.calculate_hash(str, "test_value", node_type=type(value_node))

            # Verify node exists in index
            assert value_node.node_id in _.index_data.node_to_hash
            assert hash_value in _.index_data.hash_to_node
            assert hash_value in _.index_data.values_by_type[str]
            assert hash_value in _.index_data.type_by_value

            assert _.index_data.json() == { 'hash_to_node'  : {'3f2e519923'   : value_node_id   },
                                            'node_to_hash'  : {value_node_id  : '3f2e519923'    },
                                            'type_by_value' : {'3f2e519923'   : 'builtins.str'  },
                                            'values_by_type': { 'builtins.str': {'3f2e519923'  }}}

            # Remove node
            _.remove_value_node(value_node)
            assert _.index_data.json() == { 'hash_to_node'  : {},                   # Verify node is removed from all index structures
                                            'node_to_hash'  : {},
                                            'type_by_value' : {},
                                            'values_by_type': {}}

            assert value_node.node_id not in _.index_data.node_to_hash
            assert hash_value         not in _.index_data.hash_to_node
            assert hash_value         not in _.index_data.type_by_value

    def test_calculate_hash(self):
        with self.value_index as _:
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