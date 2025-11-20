import types
from unittest                                                       import TestCase
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import is_obj_id
from osbot_utils.utils.Objects                                      import full_type_name
from mgraph_db.providers.json.actions.MGraph__Json__Data            import MGraph__Json__Data
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph    import Domain__MGraph__Json__Graph
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node     import Domain__MGraph__Json__Node
from mgraph_db.providers.json.models.Model__MGraph__Json__Graph     import Model__MGraph__Json__Graph
from mgraph_db.providers.json.models.Model__MGraph__Json__Node      import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph   import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node    import Schema__MGraph__Json__Node
from mgraph_db.providers.json.MGraph__Json                          import MGraph__Json
from osbot_utils.utils.Dev                                          import pprint


class test_MGraph__Json__Data(TestCase):

    def setUp(self):
        self.mgraph_json = MGraph__Json()

    def test__init__(self):
        with self.mgraph_json.data() as _:
            assert type(_                 ) is MGraph__Json__Data
            assert type(_.graph           ) is Domain__MGraph__Json__Graph
            assert type(_.graph.model     ) is Model__MGraph__Json__Graph
            assert type(_.graph.model.data) is Schema__MGraph__Json__Graph
            assert type(_.graph.root      ) is types.MethodType

    def test_root_node(self):
        with self.mgraph_json.data() as _:
            assert _.graph.model.data.graph_data.root_id is None                        # at the start the root_id is not set
            root_node = _.root_node()                                                   # but calling the _.root_node() method will create it

            assert type(root_node          )             is Domain__MGraph__Json__Node
            assert type(root_node.node     )             is Model__MGraph__Json__Node
            assert type(root_node.node.data)             is Schema__MGraph__Json__Node
            assert _.graph.model.data.graph_data.root_id is not None                    # so now it exists

            root_node_id = _.graph.model.data.graph_data.root_id

            assert _.root_node_id()                      == root_node_id
            assert is_obj_id(root_node_id)               is True
            assert root_node.node.obj()                  == __(data=__(node_data = __()                                      ,
                                                                       node_id   = root_node_id                              ,
                                                                       node_type = full_type_name(Schema__MGraph__Json__Node )))
        with self.mgraph_json.export() as _:
            assert _.to_dict() is None

    def test_root_property_id(self):
        with self.mgraph_json.data() as _:
            assert _.root_property_id() is None

        with self.mgraph_json.load() as _:
            _.from_data({})

        with self.mgraph_json.data() as _:
            assert _.root_property_id() is not None

        # with self.mgraph_json.screenshot() as _:
        #     _.save().dot__just_ids()
        #     _.save().dot()




