import pytest
from datetime                                                                    import datetime, UTC
from unittest                                                                    import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                import Domain__MGraph__Node
from mgraph_db.providers.time_chain.actions.MGraph__Time_Chain__Create           import MGraph__Time_Chain__Create
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types    import Time_Chain__Year, Time_Chain__Month
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Edge     import Schema__MGraph__Time_Chain__Edge__Month
from mgraph_db.mgraph.MGraph                                                     import MGraph
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.utils.Env                                                       import load_dotenv


class test_MGraph__Time_Chain__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = False                                                         # set to true to create a screenshot per test
        cls.screenshot_file   = './time-chain-create.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.mgraph      = MGraph()                                                          # Setup fresh graph for each test
        self.time_chain  = MGraph__Time_Chain__Create(mgraph_edit=self.mgraph.edit())
        #self.time_point  = MGraph__Time_Series       (graph= self.mgraph.graph).edit()

    def tearDown(self):
        if self.screenshot_create:
            with self.mgraph.screenshot(target_file=self.screenshot_file) as screenshot:
                with screenshot.export().export_dot() as _:
                    _.set_graph__rank_dir__lr()
                    _.show_node__value()
                    #_.show_node__type_full_name()
                    _.show_edge__type()
                with screenshot as _:
                    _.save_to(self.screenshot_file)
                    _.dot()


    # def test_create_point_from_datetime(self):                                              # Test complete chain creation
    #     date_time   = datetime(2025, 2, 10, 12, 31, tzinfo=UTC)
    #     date_time_2 = datetime(2025, 2, 10, 12, 29, tzinfo=UTC)
    #     date_time_3 = datetime(2025, 2, 13, 12, 29, tzinfo=UTC)
    #     self.time_point.create_from__datetime(date_time)
    #
    #     self.time_point.create_from__datetime(date_time_2)
    #     self.time_point.create_from__datetime(date_time_3)

    def test_create_chain_from_datetime(self):                                              # Test complete chain creation
        date_time   = datetime(2025, 2, 10, 12, 31, tzinfo=UTC)
        #date_time_2 = datetime(2025, 2, 10, 12, 29, tzinfo=UTC)
        #date_time_3 = datetime(2025, 2, 13, 12, 29, tzinfo=UTC)
        root_node = self.time_chain.create_from_datetime(date_time, Obj_Id())

        #self.time_chain.create_from_datetime(date_time_2, Obj_Id())
        #self.time_chain.create_from_datetime(date_time_3, Obj_Id())
        #self.time_chain.create_chain_from_datetime(datetime(2025, 3, 10, 12, 29, tzinfo=UTC))

        assert type(root_node) is Domain__MGraph__Node                                      # Verify root node

        with self.mgraph.edit() as edit:
            assert root_node.node_data.value == "2025"                                      # Check root value
            assert root_node.node_data.value_type is Time_Chain__Year                                   # Check root type

            index = edit.index()
            nodes = index.nodes_ids__from__node_id(root_node.node_id)
            assert len(nodes) == 1                                                          # Root should only have 1 connected nodes

    def test_value_reuse(self):                                                            # Test value node reuse
        date_time_1 = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        date_time_2 = datetime(2025, 2, 10, 14, 45, tzinfo=UTC)                           # Same date, different time

        root_1 = self.time_chain.create_from_datetime(date_time_1)
        root_2 = self.time_chain.create_from_datetime(date_time_2)

        assert root_1.node_id == root_2.node_id                                            # Same year should reuse node

        with self.mgraph.edit() as edit:
            index = edit.index()
            nodes_1 = index.nodes_ids__from__node_id(root_1.node_id)
            nodes_2 = index.nodes_ids__from__node_id(root_2.node_id)
            assert nodes_1 == nodes_2

    @pytest.mark.skip("Test needs fixing to take into account that we get the last node from create_partial_chain (not the first)") # todo: see a better way to do this, since I think it will be better to return all nodes and edges created
    def test_partial_chain(self):                                                          # Test partial chain creation
        last_node = self.time_chain.create_partial_chain(year=2025, month=2)              # Create year-month only

        with self.mgraph.edit() as edit:
            index = edit.index()
            nodes = index.nodes_ids__from__node_id(last_node.node_id)
            index.print__index_data()
#            print(last_node.node_id)
#            pprint(nodes)
            return                  # todo: fix test below
            assert len(nodes) == 1                                                         # Should only have month connected

            month_node = data.node(nodes[0])
            assert month_node.node_data.value == "2"                                      # Verify month value
            assert month_node.node_data.value_type is Time_Chain__Month                         # Verify month type

    def test_chain_connections(self):                                                     # Test edge creation
        date_time = datetime(2025, 2, 10, 12, 31, tzinfo=UTC)
        root_node = self.time_chain.create_from_datetime(date_time)

        with self.mgraph.edit() as edit:
            index = edit.index()
            edges = index.edges_ids__from__node_id(root_node.node_id)
            assert len(edges) == 1                                                        # Root should have one outgoing edge

        with self.mgraph.data() as data:
            edge = data.edge(edges[0])
            assert edge.edge.data.edge_type is Schema__MGraph__Time_Chain__Edge__Month   # Verify edge type

    def test_error_handling(self):                                                       # Test error cases
        with self.assertRaises(Exception):                                               # Invalid datetime
            self.time_chain.create_from_datetime(None)

        result = self.time_chain.create_partial_chain()                                 # No components
        assert result is None                                                           # Should return None for empty chain

    def test_execution_idempotency(self):                                              # Test idempotent behavior
        date_time = datetime(2025, 2, 10, 12, 31, tzinfo=UTC)

        root_1 = self.time_chain.create_from_datetime(date_time)                 # Create chain twice
        root_2 = self.time_chain.create_from_datetime(date_time)

        with self.mgraph.edit() as edit:
            assert root_1.node_id == root_2.node_id                                    # Should reuse all nodes

            index = edit.index()
            nodes_1 = index.nodes_ids__from__node_id(root_1.node_id)
            nodes_2 = index.nodes_ids__from__node_id(root_2.node_id)
            assert nodes_1 == nodes_2                                                  # Should have identical structure