from unittest                                                            import TestCase

import pytest

from osbot_utils.utils.Dev import pprint
from mgraph_db.providers.json.actions.MGraph__Json__Query__Export__View  import MGraph__Json__Query__Export__View
from mgraph_db.query.actions.MGraph__Query__Export__View                 import MGraph__Query__Export__View
from mgraph_db.providers.json.MGraph__Json                               import MGraph__Json
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph         import Domain__MGraph__Json__Graph
from osbot_utils.utils.Json                                              import json__equals__list_and_set


class test_MGraph__Query__Export__View(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgraph_json = MGraph__Json()
        cls.test_data = { 'values': [1, 2, 3]                   ,
                          'nested': { 'name' : 'child'          ,
                                      'value': 42 }             ,
                          'items' : [{ 'id': 1, 'name': 'first' },
                                     { 'id': 2, 'name': 'second'}]}
        cls.mgraph_json.load().from_data(cls.test_data)
        cls.query = cls.mgraph_json.query().setup()


    def test__export_view__no_filter(self):
        with self.query as _:
            export_view           = MGraph__Query__Export__View(mgraph_query=_)
            view_graph            = export_view.export()
            mgraph_json__exported = MGraph__Json(graph=view_graph)
            dict__exported_graph  = mgraph_json__exported.export().to_dict()

            assert type(mgraph_json__exported) is MGraph__Json
            assert type(view_graph           ) is Domain__MGraph__Json__Graph
            assert dict__exported_graph is None


    def test__export_view__root__expanded(self):
        with self.mgraph_json.data() as _:
            root_id        = _.root_property_node().node_id
            first_nodes_id = _.graph.nodes_from(root_id) #_.index().nodes_ids__from__node_id(root_id)

        #return
        with self.query as _:
            _.add_nodes_ids(first_nodes_id)
            _.add_outgoing_edges__with_depth(5)
            export_view           = MGraph__Json__Query__Export__View(mgraph_query=_)
            view_graph            = export_view.export()
            mgraph_json__exported = MGraph__Json(graph=view_graph)

            dict__original_graph  = self.mgraph_json.export     ().to_dict()
            dict__exported_graph  = mgraph_json__exported.export().to_dict()

            assert type(mgraph_json__exported) is MGraph__Json
            assert type(view_graph           ) is Domain__MGraph__Json__Graph

            # pprint(dict__exported_graph)
            # pprint(dict__original_graph)
            assert json__equals__list_and_set(dict__original_graph, dict__exported_graph)


    @pytest.mark.skip("Needs fixing after refactoring of MGraph__Index")  # for example get_nodes_by_field() doesn't exist any more
    def test__export_view__with_filter(self):
        test_data = { 'values': [1, 2, 3]                   ,
                      'nested': { 'name' : 'here'           ,
                                  'value': 42 ,
                                  'another': {'level': {'with': {'an': {'array':[1,2,3]}}}}},
                      'items' : [{ 'id': 1, 'name': 'first' },
                                 { 'id': 2, 'name': 'second'}]}
        fields_to_export = set(test_data)
        for field_to_export in fields_to_export:
            mgraph_json__original = MGraph__Json()
            mgraph_json__original.load().from_data(test_data)

            with mgraph_json__original.query().setup() as _:
                _.field(field_to_export)
                _.add_outgoing_edges__with_depth(12)
                export_view            = MGraph__Json__Query__Export__View(mgraph_query=_)
                domain_graph_exported  = export_view.export()
                mgraph_json__exported = MGraph__Json(graph=domain_graph_exported)

                exported_dict = mgraph_json__exported.export().to_dict()
                expected_data = {field_to_export: test_data[field_to_export]}
                assert json__equals__list_and_set(exported_dict, expected_data)

                #mgraph_json__exported.screenshot().save_to(f'./exported-{field_to_export}.png').dot()