from unittest                                                       import TestCase
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Objects                                      import base_types
from mgraph_db.query.models.Model__MGraph__Query__View              import Model__MGraph__Query__View
from mgraph_db.query.schemas.Schema__MGraph__Query__View            import Schema__MGraph__Query__View
from mgraph_db.query.schemas.Schema__MGraph__Query__View__Data      import Schema__MGraph__Query__View__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id


class test_Model_MGraph__Query__View(TestCase):

    def setUp(self):
        self.view_id    = Obj_Id()
        self.nodes_ids  = {Obj_Id(), Obj_Id()}
        self.edges_ids  = {Obj_Id(), Obj_Id()}
        self.operation  = 'test_operation'
        self.params     = {'param1': 'value1'}
        self.view_data  = Schema__MGraph__Query__View__Data( nodes_ids       = self.nodes_ids  ,
                                                             edges_ids       = self.edges_ids  ,
                                                             query_operation = self.operation  ,
                                                             query_params    = self.params,    )
        self.query_view = Schema__MGraph__Query__View      ( view_id         = self.view_id    ,
                                                             view_data       = self.view_data  )
        self.model_view = Model__MGraph__Query__View       ( data            = self.query_view )

    def test__setUp(self):                                                                                                  # Test basic initialization
        with self.model_view as _:
            assert type      (_)  is Model__MGraph__Query__View
            assert base_types(_)  == [Type_Safe, object]
            assert _.view_id  ()  == self.view_id
            assert _.nodes_ids()  == self.nodes_ids
            assert _.edges_ids()  == self.edges_ids
            assert _.obj      ()  == __(data     = __(view_id   = _.data.view_id                            ,
                                                      view_data = __( edges_ids        = list(_.data.view_data.edges_ids) ,
                                                                      next_view_ids    = []                               ,
                                                                      nodes_ids        = list(_.data.view_data.nodes_ids) ,
                                                                      previous_view_id = None                             ,
                                                                      query_operation  = 'test_operation'                 ,
                                                                      query_params     =__(param1='value1')               ,
                                                                      timestamp        = _.data.view_data.timestamp       )))




    def test_query_metadata(self):                                              # Test query operation metadata
        assert self.model_view.query_operation() == self.operation
        assert self.model_view.query_params()    == self.params

    def test_view_navigation(self):                                             # Test navigation properties
        assert self.model_view.previous_view_id() is None
        assert self.model_view.next_view_ids()    == set()
