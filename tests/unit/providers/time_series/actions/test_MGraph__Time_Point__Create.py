from datetime                                                                               import datetime, UTC
from unittest                                                                               import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                                           import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                           import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data                             import Schema__MGraph__Node__Value__Data
from mgraph_db.providers.time_series.MGraph__Time_Series                                    import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Builder                    import MGraph__Time_Point__Builder
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Create                     import MGraph__Time_Point__Create
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Created__Objects   import Schema__MGraph__Time_Point__Created__Objects
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges             import \
    Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Second, \
    Schema__MGraph__Time_Series__Edge__Month, Schema__MGraph__Time_Series__Edge__Day, \
    Schema__MGraph__Time_Series__Edge__Hour, Schema__MGraph__Time_Series__Edge__Minute, \
    Schema__MGraph__Time_Series__Edge__UTC_Offset, Schema__MGraph__Time_Series__Edge__Source_Id, \
    Schema__MGraph__Time_Series__Edge__Timestamp
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.utils.Env                                                                  import load_dotenv


class test_MGraph__Time_Point__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = False            # set to true to create a screenshot per test
        cls.screenshot_file   = './time-point-create.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.mgraph            = MGraph__Time_Series()                                         # Setup fresh graph for each test
        self.time_point_create = MGraph__Time_Point__Create(mgraph_edit  = self.mgraph.edit())
        self.builder           = MGraph__Time_Point__Builder()

    def tearDown(self):
        if self.screenshot_create:
            with self.mgraph.screenshot(target_file=self.screenshot_file) as screenshot:
                with screenshot.export().export_dot() as _:
                    #_.set_graph__layout_engine__fdp()
                    _.show_node__value()
                    #_.show_node__type()
                    #_.show_edge__type()
                    #_.show_edge__id()
                    _.set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Second, 'azure')
                with screenshot as _:
                    _.save_to(self.screenshot_file)
                    _.dot()

    def test_create_simple_time_point(self):                                                  # Test basic creation
        date_time     = datetime(2025, 2, 10, 12, 31, tzinfo=UTC)
        date_time_str = "Mon, 10 Feb 2025 12:31:00 +0000"
        create_data   = self.builder.from_datetime(date_time)
        time_objects  = self.time_point_create.execute(create_data)

        assert type(time_objects) is Schema__MGraph__Time_Point__Created__Objects

        with self.mgraph.data() as data:                                                      # Verify node creation
            time_point = data.node(time_objects.time_point__node_id)
            assert time_point.node_data.value == date_time_str

            for edge_id in time_objects.value_edges__by_type.values():                              # Verify edge creation
                assert data.edge(edge_id) is not None

            for node_id in time_objects.value_nodes__by_type.values():                                  # Verify value nodes
                assert data.node(node_id) is not None

    def test_value_reuse(self):                                                               # Test value node reuse
        test_time               = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data_1           = self.builder.from_datetime(test_time)                                # Create first time point
        create_data_1.source_id = Obj_Id()                                                              # todo: find a better way to assign this ID
        created_objects_1       = self.time_point_create.execute(create_data_1)
        create_data_2           = self.builder.from_datetime(test_time)                                # Create second time point
        created_objects_2       = self.time_point_create.execute(create_data_2)

        year_edge_type          = Schema__MGraph__Time_Series__Edge__Year  # Check year value reuse

        #self.mgraph.index().print__index_data()
        assert len(created_objects_1.value_nodes__by_type) == 8
        assert len(created_objects_1.value_edges__by_type) == 8
        assert list(created_objects_1.value_nodes__by_type) == [Schema__MGraph__Time_Series__Edge__Year     ,
                                                                Schema__MGraph__Time_Series__Edge__Month    ,
                                                                Schema__MGraph__Time_Series__Edge__Day      ,
                                                                Schema__MGraph__Time_Series__Edge__Hour     ,
                                                                Schema__MGraph__Time_Series__Edge__Minute   ,
                                                                Schema__MGraph__Time_Series__Edge__Second   ,
                                                                Schema__MGraph__Time_Series__Edge__Source_Id,
                                                                Schema__MGraph__Time_Series__Edge__Timestamp]
        assert list(created_objects_1.value_nodes__by_type) == list(created_objects_1.value_edges__by_type)
        assert created_objects_1.value_nodes__by_type[year_edge_type] == created_objects_2.value_nodes__by_type[year_edge_type]

    def test_timezone_handling(self):                                                         # Test timezone components
        test_time   = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        time_objects = self.time_point_create.execute(create_data)
        assert time_objects.timezone__node_id is not None
        assert time_objects.timezone__edge_id is not None

        with self.mgraph.data() as data:                                                      # Verify timezone node
            timezone_node = data.node(time_objects.timezone__node_id)
            assert timezone_node.node_data.value == "UTC"

    def test_partial_time_point(self):                                                        # Test partial time components
        create_data = self.builder.from_components(year=2025, month=2)                        # Only year and month
        time_objects = self.time_point_create.execute(create_data)

        with self.mgraph.data() as data:
            created_edges = [data.edge(edge_id) for edge_id in time_objects.value_edges__by_type.values()]
            assert len(created_edges) == 2                                                     # Should only have year and month edges

    def test_utc_offset_creation(self):                                                       # Test UTC offset handling
        test_time = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        created_objects = self.time_point_create.execute(create_data)

        utc_node_id     = created_objects.utc_offset__node_id
        utc_node        = self.mgraph.data().node(utc_node_id)
        utc_edge_id     = created_objects.utc_offset__edge_id
        utc_edge        = self.mgraph.data().edge(utc_edge_id)

        assert type(utc_node_id       ) is Node_Id
        assert type(utc_edge_id       ) is Edge_Id
        assert type(utc_node          ) is Domain__MGraph__Node
        assert type(utc_node.node_data) is Schema__MGraph__Node__Value__Data
        assert utc_node.node_data.value == '0'
        assert type(utc_edge          ) is Domain__MGraph__Edge
        assert utc_edge.edge_type       is Schema__MGraph__Time_Series__Edge__UTC_Offset

        with self.mgraph.index() as _:
            assert utc_edge_id in _.edges_ids__to__node_id(utc_node_id)

    def test_index_updates(self):                                                             # Test index maintenance
        test_time   = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        self.time_point_create.execute(create_data)                                           # Create time point

        index = self.time_point_create.mgraph_edit.index()
        assert len(index.nodes_by_type()) > 0                                                 # Verify index has been updated
        assert len(index.edges_by_type()) > 0

    def test_error_cases(self):                                                               # Test error handling
        with self.assertRaises(Exception):                                                    # Invalid create data
            self.time_point_create.execute(None)

        create_data = self.builder.from_components()                                          # Empty create data
        create_objects = self.time_point_create.execute(create_data)
        assert len(create_objects.value_edges__by_type) == 0                                    # Should create time point but no components

    def test_execution_idempotency(self):                                                     # Test idempotent behavior
        test_time = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        objects_1 = self.time_point_create.execute(create_data)                               # Execute twice
        objects_2 = self.time_point_create.execute(create_data)

        assert objects_1.time_point__node_id != objects_2.time_point__node_id                             # Should create new time point
        assert objects_1.value_nodes__by_type == objects_2.value_nodes__by_type                               # But reuse value nodes

        # self.time_point_create.execute(create_data)
        # self.time_point_create.execute(create_data)
        # self.time_point_create.execute(create_data)
        # self.time_point_create.execute(create_data)


