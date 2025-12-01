from unittest                                                               import TestCase
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List      import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property  import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value     import Schema__MGraph__Json__Node__Value
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.utils.Json                                                 import json__equals__list_and_set
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id            import Obj_Id
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node             import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict       import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict      import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.MGraph__Json                                  import MGraph__Json


class test_MGraph__Json__Edit(TestCase):

    def setUp(self):
        self.mgraph_json = MGraph__Json()

    def test_add_root_property_node(self):
        with self.mgraph_json.edit() as _:
            root_property_node = _.add_root_property_node()
            assert type(root_property_node) == Domain__MGraph__Json__Node__Dict

        with self.mgraph_json.export() as _:
            assert _.to_dict() == {}

        with self.mgraph_json.data()  as _:
            assert _.root_property_id() == root_property_node.node_id

            root_property_node =  _.root_property_node()
            assert type(root_property_node          ) == Domain__MGraph__Json__Node                 # this is the generic  Node type        todo: explore the side effects that this is not an object of type Domain__MGraph__Json__Node__Dict
            assert type(root_property_node.node     ) == Model__MGraph__Json__Node__Dict            # this is the specific Node__Dict type
            assert type(root_property_node.node.data) == Schema__MGraph__Json__Node__Dict           # this is the specific Node__Dict type


    def test_add_property(self):
        assert self.mgraph_json.export().to_dict() is None
        with self.mgraph_json.edit() as _:

            root_property_node    = _.add_root_property_node()
            root_property_node_id = root_property_node.node_id
            new_property_1        = _.add_property('abc' , node_id=root_property_node_id             )      # add property with no value
            new_property_2        = _.add_property('1234', node_id=root_property_node_id, value='xyz')      # add property with value
            value_node            = _.add_value  ('12345', node_id=new_property_1.node_id            )      # add value to the property with no value

            assert type(root_property_node   ) is Domain__MGraph__Json__Node__Dict
            assert type(root_property_node_id) is Node_Id
            assert type(new_property_1       ) is Domain__MGraph__Json__Node
            assert type(new_property_2       ) is Domain__MGraph__Json__Node
            assert type(value_node           ) is Domain__MGraph__Json__Node

        assert self.mgraph_json.export().to_dict() == {'1234': 'xyz', 'abc': '12345'}               # confirm values set correctly

    def test_add_list(self):
        assert self.mgraph_json.export().to_dict() is None
        with self.mgraph_json.edit() as _:
            root_property_node    = _.add_root_property_node()
            new_property_1        = _.add_property('abc', node_id=root_property_node.node_id)
            export__step_1        = self.mgraph_json.export().to_dict()

            new_list_1            = _.add_list(node_id=new_property_1.node_id              )
            export__step_2        = self.mgraph_json.export().to_dict()

            new_value_1           = _.add_value(value='an_value', node_id=new_list_1.node_id)
            export__step_3        = self.mgraph_json.export().to_dict()

            new_list_2            = _.add_list(node_id=new_list_1.node_id                  )
            export__step_4        = self.mgraph_json.export().to_dict()

            new_dict_1            = _.add_dict(node_id=new_list_1.node_id                  )
            export__step_5        = self.mgraph_json.export().to_dict()

            new_property_2        = _.add_property('abc' , node_id=new_dict_1.node_id , value='a')
            export__step_6        = self.mgraph_json.export().to_dict()

            new_property_3        = _.add_property('def' , node_id=root_property_node.node_id )
            export__step_7        = self.mgraph_json.export().to_dict()

            new_dict_2            = _.add_dict(node_id=new_property_3.node_id)
            export__step_8        = self.mgraph_json.export().to_dict()

            root_node_id = _.data().root_node_id()
            new_list_3           = _.add_list(node_id=root_node_id)

            export__step_9       = self.mgraph_json.export().to_dict()              # this will have no effect on the output
            new_value_2          = _.add_value('a', node_id=root_node_id)

            export__step_10 = self.mgraph_json.export().to_dict()                   # this will have no effect on the output (I just wanted to have a full schema :) )

            assert type(root_property_node      ) is Domain__MGraph__Json__Node__Dict
            assert type(new_property_1.node.data) is Schema__MGraph__Json__Node__Property
            assert type(new_list_1.node.data    ) is Schema__MGraph__Json__Node__List
            assert type(new_value_1.node.data   ) is Schema__MGraph__Json__Node__Value
            assert type(new_list_2.node.data    ) is Schema__MGraph__Json__Node__List
            assert type(new_dict_1.node.data    ) is Schema__MGraph__Json__Node__Dict
            assert type(new_property_2.node.data) is Schema__MGraph__Json__Node__Property
            assert type(new_property_3.node.data) is Schema__MGraph__Json__Node__Property
            assert type(new_dict_2.node.data    ) is Schema__MGraph__Json__Node__Dict
            assert type(new_list_3.node.data    ) is Schema__MGraph__Json__Node__List
            assert type(new_value_2.node.data   ) is Schema__MGraph__Json__Node__Value

        assert export__step_1 == {'abc': None}
        assert export__step_2 == {'abc': []}
        assert export__step_3 == {'abc': ['an_value']}
        assert json__equals__list_and_set(export__step_4, {'abc': ['an_value', []               ]             }) is True
        assert json__equals__list_and_set(export__step_5, {'abc': ['an_value', [], {}           ]             }) is True
        assert json__equals__list_and_set(export__step_6, {'abc': ['an_value', [], {'abc': 'a' }]             }) is True
        assert json__equals__list_and_set(export__step_7, {'abc': ['an_value', [], {'abc': 'a' }], 'def': None}) is True
        assert json__equals__list_and_set(export__step_8, {'abc': ['an_value', [], {'abc': 'a' }], 'def': {}  }) is True
        assert export__step_8 == export__step_9
        assert export__step_9 == export__step_10



    def test_add_property__just_one(self):
        with self.mgraph_json.edit() as _:
            root_property_node    = _.add_root_property_node()
            new_property_1        = _.add_property('abc' , node_id=root_property_node.node_id             )      # add property with no value

            assert type(new_property_1) is Domain__MGraph__Json__Node

        assert self.mgraph_json.export().to_dict() == {'abc': None}

    def test_add_dict_to_property(self):
        with self.mgraph_json.edit() as _:
            root_property_node = _.add_root_property_node()
            export__step_1     = self.mgraph_json.export().to_dict()
            new_property_1     = _.add_property('parent'  , node_id=root_property_node.node_id)
            export__step_2     = self.mgraph_json.export().to_dict()
            new_dict_1         = _.add_dict     (node_id=new_property_1.node_id    )
            export__step_3     = self.mgraph_json.export().to_dict()
            new_property_2     = _.add_property('without_value', node_id=new_dict_1.node_id )
            export__step_4     = self.mgraph_json.export().to_dict()
            new_property_3     = _.add_property('with_value'   , node_id=new_dict_1.node_id , value='an-value')
            export__step_5     = self.mgraph_json.export().to_dict()

            assert type(new_property_1) == Domain__MGraph__Json__Node
            assert type(new_property_2) == Domain__MGraph__Json__Node
            assert type(new_property_3) == Domain__MGraph__Json__Node
            
            assert export__step_1 == {}
            assert export__step_2 == {'parent': None                                                 }
            assert export__step_3 == {'parent': {}                                                   }
            assert export__step_4 == {'parent': {'without_value': None                              }}
            assert export__step_5 == {'parent': {'with_value'   : 'an-value', 'without_value': None }}

        assert self.mgraph_json.export().to_dict() == {'parent': {'with_value'   : 'an-value',
                                                                  'without_value': None      }}

    # self.mgraph_json.screenshot().save().dot__just_ids   ()
    # self.mgraph_json.screenshot().save().dot__just_types()
    # self.mgraph_json.screenshot().save().dot__schema()
    # self.mgraph_json.screenshot().save().dot()

    # def test_show(self):
    #     test_data = {'a': {'b':123}}
    #     self.mgraph_json.load().from_data(test_data)
    #     self.mgraph_json.screenshot().save().dot__just_types()
    #     assert self.mgraph_json.export().to_dict() == test_data