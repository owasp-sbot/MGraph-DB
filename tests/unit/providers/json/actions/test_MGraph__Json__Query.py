import pytest
from unittest                                                   import TestCase
from osbot_utils.testing.__                                     import __
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.testing.__helpers                              import obj
from mgraph_db.providers.json.MGraph__Json                      import MGraph__Json
from mgraph_db.providers.json.actions.MGraph__Json__Query       import MGraph__Json__Query

class test_MGraph__Json__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Needs fixing after refactoring of MGraph__Index") # todo: for example get_nodes_by_field() doesn't exist any more

    def setUp(self):
        self.mgraph    = MGraph__Json()
        self.test_data = {  'name'  : 'root'                      ,
                            'values': [1, 2, 3]                   ,
                            'nested': { 'name' : 'child'          ,
                                        'value': 42 }             ,
                            'items' : [{ 'id': 1, 'name': 'first' },
                                       { 'id': 2, 'name': 'second'}]}

        self.mgraph.load().from_data(self.test_data)
        self.json_query = MGraph__Json__Query(mgraph_data=self.mgraph.data(), mgraph_index=self.mgraph.index()).setup()

    def test_value_access(self):
        with self.mgraph.edit() as _:
            root_id = _.root_property_node_id()
        with self.json_query as json_query:
            assert obj(json_query.stats()) == __(source_graph = __( nodes      = 27      ,
                                                                    edges      = 26      ),
                                                 current_view = __( has_next   = False   ,
                                                                    has_prev   = False   ,
                                                                    operation  ='initial',
                                                                    params     = __()    ,
                                                                    view_edges = 0      ,
                                                                    view_nodes = 0      ))
            assert len(json_query.edges_ids()) == 0
            assert len(json_query.nodes_ids()) == 0
            json_query.add_node_id(root_id)

            query_nested = json_query  ['nested']

            assert obj(json_query.stats()) == __(source_graph = __( nodes      = 27              ,
                                                                    edges      = 26              ),
                                                 current_view = __( has_next   = False           ,
                                                                    has_prev   = True            ,
                                                                    operation  ='dict_access'    ,
                                                                    params     = __(key='nested'),
                                                                    view_edges = 3               ,
                                                                    view_nodes = 1               ))
            assert len(json_query.edges_ids()) == 3
            assert len(json_query.nodes_ids()) == 1

            query_value = query_nested['value' ]

            assert obj(json_query.stats()) == __(source_graph = __( nodes      = 27              ,
                                                                    edges      = 26              ),
                                                 current_view = __( has_next   = False           ,
                                                                    has_prev   = True            ,
                                                                    operation  ='dict_access'    ,
                                                                    params     = __(key='value'),
                                                                    view_edges = 1               ,
                                                                    view_nodes = 1               ))
            assert len(json_query.edges_ids()) == 1
            assert len(json_query.nodes_ids()) == 1
            assert query_value.value       () == 42

            json_query.reset()
            assert obj(json_query.stats()) == __(source_graph = __( nodes      = 27      ,
                                                                    edges      = 26      ),
                                                 current_view = __( has_next   = False   ,
                                                                    has_prev   = False   ,
                                                                    operation  ='initial',
                                                                    params     = __()    ,
                                                                    view_edges = 0       ,
                                                                    view_nodes = 0      ))
            json_query.add_node_id(root_id)
            assert json_query['nested']['value'].value() == 42

    def test_empty_access(self):
        with self.mgraph.data() as data:
            with MGraph__Json__Query(mgraph_data  = data,
                                     mgraph_index = self.mgraph.index()).setup() as _:
                _['nonexistent']
                assert _.stats() == { 'current_view': { 'has_next'  : False ,
                                                             'has_prev'  : True  ,
                                                             'operation' : 'empty',
                                                             'params'    : {}    ,
                                                             'view_edges': 0     ,
                                                             'view_nodes': 0     },
                                           'source_graph': { 'edges'     : 26    ,
                                                             'nodes'     : 27    }}
                assert len(_.edges_ids()) == 0
                assert len(_.nodes_ids()) == 0

                assert _.value() is None

    def test_view_navigation(self):
        with self.mgraph.edit() as _:
            root_id = _.root_property_node_id()
            self.json_query.add_node_id(root_id)

        with self.mgraph.data() as data:
            result = self.json_query['nested']['value']                                 # Navigate through views
            assert result.value() == 42
            assert self.json_query.current_view().query_operation() == 'dict_access'
            assert self.json_query.current_view().query_params   () == {'key': 'value'}

            assert self.json_query.go_back()                        is True                                            # Go back to previous view
            assert self.json_query['name'].value() == 'child'
            assert self.json_query.current_view().query_operation() == 'dict_access'
            assert self.json_query.current_view().query_params   () == {'key': 'name'}

            assert self.json_query.go_back()                        is True                                # Go back to root
            assert self.json_query.current_view().query_operation() == 'dict_access'
            assert self.json_query.current_view().query_params   () == {'key': 'nested'}

            assert self.json_query.go_back()                        is True
            assert self.json_query.current_view().query_operation() == 'add_node_id'
            assert self.json_query.current_view().query_params   () == {'node_id': root_id}

            assert self.json_query.go_back()                        is True
            assert self.json_query.current_view().query_operation() == 'initial'
            assert self.json_query.current_view().query_params   () == {}

            assert self.json_query.go_back()                        is False
            assert self.json_query.current_view().query_operation() == 'initial'
            assert self.json_query.current_view().query_params   () == {}

    def test__bug__array_item_access(self):
        self.json_query['values'][1]
        #self.json_query.print_stats()
        assert self.json_query.value() is None          # BUG: should be two
        # assert self.json_query.value() == 2

    def test__bug__name_property_access(self):
        with self.json_query as _:
            _.name('child')
            assert _.exists() is False
            assert _.value() != 'child'         # BUG should be 'child'
            assert _.value() is None            # BUG should not be None



    @pytest.mark.skip('to wire up when we have figured how what happens with .dict()')
    def test_dict_access(self):
        result = MGraph__Json__Query(mgraph_data  = self.mgraph.data(),
                                     mgraph_index = self.mgraph.index())
        assert result.dict() == self.test_data

    @pytest.mark.skip('to wire up when we have figured how what happens with .list()')
    def test_list_access(self):
        with self.mgraph.data() as data:
            result = MGraph__Json__Query(mgraph_data=data,
                                         mgraph_index=self.mgraph.index)['values']
            assert result.list() == [1, 2, 3]

    @pytest.mark.skip('to wire up when we have figured how what happens with .dict()')
    def test_nested_dict_access(self):
        with self.mgraph.data() as data:
            result = MGraph__Json__Query(mgraph_data=data,
                                       mgraph_index=self.mgraph.index,)['nested']
            assert result.dict() == {'name': 'child', 'value': 42}



    @pytest.mark.skip('to wire up when we have figured how what happens with .dict()')
    def test_complex_array_access(self):
        with self.mgraph.data() as data:
            result = MGraph__Json__Query(mgraph_data=data,
                                       mgraph_index=self.mgraph.index,
                                       query_views=self.mgraph.views)['items'][0]
            assert result.dict() == {'id': 1, 'name': 'first'}




    @pytest.mark.skip('to wire up when we have figured how what happens with .dict()')
    def test_invalid_access(self):
        # Access dict as list
        result = self.json_query['name'].list()
        assert result == []

        # Access list as dict
        result = self.json_query['values'].dict()
        assert result == {}

        # Access out of bounds
        result = self.json_query['values'][10].value()
        assert result is None


    @pytest.mark.skip("fix index access")
    def test__bug__performance(self):
        with capture_duration() as duration:

            for _ in range(100):                                    # Multiple operations
                result = self.json_query['items'][0]['name'].value()
                assert result == 'first'

                result = self.json_query['nested']['value'].value()
                assert result == 42

                result = self.json_query['values'][1].value()
                assert result == 2

        assert duration.seconds < 1.0  # Should complete in under 1 second