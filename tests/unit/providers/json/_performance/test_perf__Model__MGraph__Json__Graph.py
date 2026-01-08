import uuid
import pytest
from unittest                                                                       import TestCase
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import is_obj_id, Obj_Id
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Edge                     import Domain__MGraph__Json__Edge
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph                    import Domain__MGraph__Json__Graph
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node                     import Domain__MGraph__Json__Node
from mgraph_db.providers.json.models.Model__MGraph__Json__Edge                      import Model__MGraph__Json__Edge
from mgraph_db.providers.json.models.Model__MGraph__Json__Graph                     import Model__MGraph__Json__Graph
from mgraph_db.providers.json.models.Model__MGraph__Json__Node                      import Model__MGraph__Json__Node
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict                import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List                import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Property            import Model__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge                    import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph                   import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node                    import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict              import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List              import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property          import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data    import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value             import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data       import Schema__MGraph__Json__Node__Value__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Types                   import Schema__MGraph__Json__Types
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


from osbot_utils.helpers.performance.Performance_Measure__Session import Performance_Measure__Session


class test_perf__Model__MGraph__Json__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = True
        cls.session     = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.model_graph = Model__MGraph__Json__Graph()

    def test_Obj_Id(self):
        class An_Class(Type_Safe):
            an_id: Obj_Id

        new_guid = Obj_Id()
        def new_object():
            new_obj                   = object.__new__(An_Class)
            new_obj.__dict__['an_id'] = new_guid
            return new_obj

        def new_uuid4():
            return str(uuid.uuid4())


        # with self.session as _:
        #     print()
        #     print()
        #     _.measure(An_Class   ).print(15)
        #     _.measure(Random_Guid).print(15)
        #     _.measure(random_guid).print(15)
        #     _.measure(uuid.uuid4 ).print(15)
        #     _.measure(new_uuid4  ).print(15)
        #     _.measure(new_object ).print(15)

        an_class = new_object()
        assert an_class.json()            == {'an_id': new_guid}
        assert an_class.obj ()            == __(an_id = new_guid)
        assert type     (an_class         ) is An_Class
        assert type     (an_class.an_id   ) is Obj_Id
        assert is_obj_id(an_class.an_id) is True


    def test__Schema__MGraph__Json__Node(self):
        with self.session as _:
            print()
            print()
            _.measure(Schema__MGraph__Json__Node).print().assert_time__less_than(30_000)

    @pytest.mark.skip("heavy test")
    def test_measure_main_types_of_objects(self):
        with self.session as _:
            print()
            _.measure(self.model_graph.new_node           ).print(36)
            _.measure(Domain__MGraph__Json__Graph         ).print(36)
            _.measure(Domain__MGraph__Json__Edge          ).print(36)
            _.measure(Domain__MGraph__Json__Node          ).print(36)
            print()
            _.measure(Model__MGraph__Json__Graph          ).print(36)
            _.measure(Model__MGraph__Json__Edge           ).print(36)
            _.measure(Model__MGraph__Json__Node           ).print(36)
            _.measure(Model__MGraph__Json__Node__Dict     ).print(36)
            _.measure(Model__MGraph__Json__Node__Property ).print(36)
            _.measure(Model__MGraph__Json__Node__List     ).print(36)
            print()
            _.measure(Schema__MGraph__Json__Graph         ).print(36)
            _.measure(Schema__MGraph__Json__Edge          ).print(36)
            _.measure(Schema__MGraph__Json__Node          ).print(36)
            _.measure(Schema__MGraph__Json__Node__Dict    ).print(36)
            _.measure(Schema__MGraph__Json__Node__Property).print(36)
            _.measure(Schema__MGraph__Json__Node__List    ).print(36)
            _.measure(Schema__MGraph__Json__Node__Value   ).print(36)
            _.measure(Schema__MGraph__Json__Types         ).print(36)
            print()
            _.measure(Schema__MGraph__Json__Node__Property__Data).print(42)
            _.measure(Schema__MGraph__Json__Node__Value__Data   ).print(42)

# on 20th Jan 2025
# ============================== 1 passed in 2.59s ===============================
# PASSED [100%]
# new_node                             | score: 100,000 ns  | raw: 110,736 ns
# Domain__MGraph__Json__Graph          | score: 200,000 ns  | raw: 167,122 ns
# Domain__MGraph__Json__Edge           | score: 200,000 ns  | raw: 228,636 ns
# Domain__MGraph__Json__Node           | score: 200,000 ns  | raw: 194,428 ns
#
# Model__MGraph__Json__Graph           | score: 100,000 ns  | raw: 133,453 ns
# Model__MGraph__Json__Edge            | score:  90,000 ns  | raw:  87,976 ns
# Model__MGraph__Json__Node            | score:  50,000 ns  | raw:  50,300 ns
# Model__MGraph__Json__Node__Dict      | score:  50,000 ns  | raw:  53,807 ns
# Model__MGraph__Json__Node__Property  | score:  60,000 ns  | raw:  56,310 ns
# Model__MGraph__Json__Node__List      | score:  50,000 ns  | raw:  54,632 ns
#
# Schema__MGraph__Json__Graph          | score: 100,000 ns  | raw:  99,461 ns
# Schema__MGraph__Json__Edge           | score:  70,000 ns  | raw:  74,515 ns
# Schema__MGraph__Json__Node           | score:  40,000 ns  | raw:  36,679 ns
# Schema__MGraph__Json__Node__Dict     | score:  40,000 ns  | raw:  38,378 ns
# Schema__MGraph__Json__Node__Property | score:  40,000 ns  | raw:  40,801 ns
# Schema__MGraph__Json__Node__List     | score:  40,000 ns  | raw:  38,802 ns
# Schema__MGraph__Json__Node__Value    | score:  40,000 ns  | raw:  41,138 ns
# Schema__MGraph__Json__Types          | score:  30,000 ns  | raw:  28,673 ns
#
# Schema__MGraph__Json__Node__Property__Data | score:   3,000 ns  | raw:   2,710 ns
# Schema__MGraph__Json__Node__Value__Data    | score:   4,000 ns  | raw:   3,757 ns



import random



#_hex_table = [f"{i:02x}" for i in range(256)]
#
#
#
# def test_performance_3():
#     def generate_32():
#         random.getrandbits(32)
#
#     def via_format():
#         return f"{random.getrandbits(32):08x}"  # pad to 8 chars with leading zeros
#
#     def via_hex():
#         return hex(random.getrandbits(32))[2:].zfill(8)  # slice off '0x' and pad
#
#     def old_way():
#         bits = random.getrandbits(32)
#         return (_hex_table[bits & 0xFF] +
#                 _hex_table[(bits >> 8) & 0xFF] +
#                 _hex_table[(bits >> 16) & 0xFF] +
#                 _hex_table[(bits >> 24) & 0xFF])
#
#     def new_uuid4():
#         return str(uuid.uuid4())
#
#     def random_guid():
#         return Random_Guid()
#
#
#
#     with Performance_Measure__Session() as session:
#         print()
#         print("\nPerformance Comparison:")
#         session.measure(generate_32).print(15)
#         session.measure(via_format ).print(15)
#         session.measure(via_hex    ).print(15)
#         session.measure(old_way    ).print(15)
#         session.measure(new_uuid4  ).print(15)
#         session.measure(random_guid).print(15)



