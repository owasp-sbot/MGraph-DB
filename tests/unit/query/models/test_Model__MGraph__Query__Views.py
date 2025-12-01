from unittest                                                       import TestCase
from mgraph_db.query.models.Model__MGraph__Query__Views             import Model__MGraph__Query__Views
from mgraph_db.query.schemas.Schema__MGraph__Query__Views           import Schema__MGraph__Query__Views
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.utils.Objects                                      import base_types
from mgraph_db.query.models.Model__MGraph__Query__View              import Model__MGraph__Query__View
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
class test_Model__MGraph__Query__Views(TestCase):

    def setUp(self):
        self.views_data = Schema__MGraph__Query__Views( views           = {}             ,
                                                        first_view_id   = None           ,
                                                        current_view_id = None           )
        self.query_views = Model__MGraph__Query__Views( data            = self.views_data)
        self.nodes_ids  = { Node_Id(Obj_Id()), Node_Id(Obj_Id())}
        self.edges_ids  = { Edge_Id(Obj_Id()), Edge_Id(Obj_Id())}

    def test_init(self):                                                                            # Test basic initialization
        assert type(self.query_views)                is Model__MGraph__Query__Views
        assert base_types(self.query_views)          == [Type_Safe, object]
        assert len(self.query_views.data.views)      == 0
        assert self.query_views.data.first_view_id   is None
        assert self.query_views.data.current_view_id is None

    def test_add_view(self):                                                                        # Test adding a view
        view = self.query_views.add_view(nodes_ids  = self.nodes_ids   ,
                                         edges_ids  = self.edges_ids   ,
                                         operation  = 'test_op'        ,
                                         params     = {'test': 'value'})

        assert type(view)                            is Model__MGraph__Query__View
        assert view.nodes_ids()                      == self.nodes_ids
        assert view.edges_ids()                      == self.edges_ids
        assert view.query_operation()                == 'test_op'
        assert view.query_params()                   == {'test': 'value'}
        assert view.previous_view_id()               is None
        assert view.next_view_ids()                  == set()
        assert self.query_views.data.first_view_id   == view.view_id()
        assert self.query_views.data.current_view_id == view.view_id()

    def test_view_chain(self):                                                  # Test view chain creation
        view1 = self.query_views.add_view(nodes_ids = self.nodes_ids,
                                         edges_ids  = self.edges_ids,
                                         operation  = 'op1'         ,
                                         params     = {}            )

        view2 = self.query_views.add_view(nodes_ids   = self.nodes_ids ,
                                          edges_ids   = self.edges_ids ,
                                          operation   = 'op2'          ,
                                          params      = {}             ,
                                          previous_id = view1.view_id())

        assert view2.previous_view_id()               == view1.view_id()
        assert view1.next_view_ids()                  == {view2.view_id()}
        assert self.query_views.data.first_view_id    == view1.view_id()
        assert self.query_views.data.current_view_id  == view2.view_id()

    def test_view_navigation(self):                                             # Test view navigation
        view1 = self.query_views.add_view(nodes_ids   = self.nodes_ids ,
                                          edges_ids   = self.edges_ids ,
                                          operation   = 'op1'          ,
                                          params      = {}             )
        view2 = self.query_views.add_view(nodes_ids   = self.nodes_ids ,
                                          edges_ids   = self.edges_ids ,
                                          operation   = 'op2'          ,
                                          params      = {}             ,
                                          previous_id = view1.view_id())

        assert self.query_views.current_view().view_id()   == view2.view_id()
        self.query_views.set_current_view(view1.view_id())                      # Test setting current view
        assert self.query_views.current_view().view_id()   == view1.view_id()
        assert self.query_views.set_current_view(Obj_Id()) is False             # Test invalid view ID

    def test_view_removal(self):                                                # Test view removal
        view_1 = self.query_views.add_view(nodes_ids   = self.nodes_ids  ,
                                           edges_ids   = self.edges_ids  ,
                                           operation   = 'op1'           ,
                                           params      = {}              )
        view_2 = self.query_views.add_view(nodes_ids   = self.nodes_ids  ,
                                           edges_ids   = self.edges_ids  ,
                                           operation   = 'op2'           ,
                                           params      = {}              ,
                                           previous_id = view_1.view_id() )
        view_3 = self.query_views.add_view(nodes_ids   = self.nodes_ids  ,
                                           edges_ids   = self.edges_ids  ,
                                           operation   = 'op3'           ,
                                           params      = {}              ,
                                           previous_id = view_2.view_id() )

        assert view_1.previous_view_id() is None
        assert view_2.previous_view_id() == view_1.view_id()
        assert view_3.previous_view_id() == view_2.view_id()
        assert view_1.next_view_ids   () == { view_2.view_id() }
        assert view_2.next_view_ids   () == { view_3.view_id() }
        assert view_3.next_view_ids   () == set()

        assert self.query_views.remove_view(view_2.view_id()) is True                # Remove middle view

        assert view_1.previous_view_id() is None

        assert view_3.previous_view_id() == view_1.view_id()
        assert view_1.next_view_ids   () == set()                                    # BUG, this should be view_3 # todo: check if this is the expected behaviour
        assert view_3.next_view_ids   () == set()

        assert view_2.next_view_ids   () == { view_3.view_id() }
        assert view_2.previous_view_id() == view_1.view_id()

        assert self.query_views.remove_view(Obj_Id()) is False                      # Test removing non-existent view