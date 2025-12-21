from unittest                                                            import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Edges                         import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                        import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Paths                         import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Types                         import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Stats                         import MGraph__Index__Stats
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Edges   import Schema__MGraph__Index__Data__Edges
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels  import Schema__MGraph__Index__Data__Labels
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Paths   import Schema__MGraph__Index__Data__Paths
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Types   import Schema__MGraph__Index__Data__Types
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats         import Schema__MGraph__Index__Stats
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats         import Schema__MGraph__Index__Stats__Connections
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats         import Schema__MGraph__Index__Stats__Summary
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats         import Schema__MGraph__Index__Stats__Paths
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Stats         import Schema__MGraph__Index__Stats__Index_Data
from osbot_utils.testing.__                                              import __
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id        import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id         import Obj_Id


class test_MGraph__Index__Stats(TestCase):

    def setUp(self):
        self.edges_data   = Schema__MGraph__Index__Data__Edges()
        self.labels_data  = Schema__MGraph__Index__Data__Labels()
        self.paths_data   = Schema__MGraph__Index__Data__Paths()
        self.types_data   = Schema__MGraph__Index__Data__Types()
        self.edges_index  = MGraph__Index__Edges (data=self.edges_data )
        self.labels_index = MGraph__Index__Labels(data=self.labels_data)
        self.paths_index  = MGraph__Index__Paths (data=self.paths_data )
        self.types_index  = MGraph__Index__Types (data=self.types_data )
        self.stats_index  = MGraph__Index__Stats(edges_index  = self.edges_index  ,
                                                  labels_index = self.labels_index ,
                                                  paths_index  = self.paths_index  ,
                                                  types_index  = self.types_index  )

    def test__init__(self):
        with self.stats_index as _:
            assert type(_)              is MGraph__Index__Stats
            assert type(_.edges_index)  is MGraph__Index__Edges
            assert type(_.labels_index) is MGraph__Index__Labels
            assert type(_.paths_index)  is MGraph__Index__Paths
            assert type(_.types_index)  is MGraph__Index__Types

    # =========================================================================
    # Stats Method Tests
    # =========================================================================

    def test_stats__empty(self):
        with self.stats_index as _:
            result = _.stats()

            assert type(result) is Schema__MGraph__Index__Stats
            assert result.summary.total_nodes == 0
            assert result.summary.total_edges == 0

    def test_stats__with_data(self):
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())

        # Add some data
        self.types_data.nodes_by_type['TestNode'] = {node_id_1, node_id_2}
        self.edges_index.index_edge(edge_id, node_id_1, node_id_2)

        with self.stats_index as _:
            result = _.stats()

            assert result.summary.total_nodes == 2
            assert result.summary.total_edges == 1
            assert result.index_data.edge_to_nodes == 1

    # =========================================================================
    # Connections Stats Tests
    # =========================================================================

    def test_connections_stats__empty(self):
        with self.stats_index as _:
            result = _.connections_stats()

            assert type(result) is Schema__MGraph__Index__Stats__Connections
            assert result.total_nodes == 0
            assert result.avg_incoming_edges == 0
            assert result.avg_outgoing_edges == 0

    def test_connections_stats__with_edges(self):
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())
        node_id_3 = Node_Id(Obj_Id())

        self.edges_index.index_edge(Edge_Id(Obj_Id()), node_id_1, node_id_2)
        self.edges_index.index_edge(Edge_Id(Obj_Id()), node_id_1, node_id_3)
        self.edges_index.index_edge(Edge_Id(Obj_Id()), node_id_2, node_id_3)

        with self.stats_index as _:
            result = _.connections_stats()

            assert result.total_nodes == 3
            assert result.max_outgoing_edges == 2                               # node_id_1 has 2 outgoing
            assert result.max_incoming_edges == 2                               # node_id_3 has 2 incoming

    # =========================================================================
    # Summary Stats Tests
    # =========================================================================

    def test_summary_stats(self):
        self.types_data.nodes_by_type['TypeA'] = {Node_Id(Obj_Id()), Node_Id(Obj_Id())}
        self.types_data.nodes_by_type['TypeB'] = {Node_Id(Obj_Id())}
        self.labels_data.edges_by_predicate['predicate1'] = {Edge_Id(Obj_Id())}

        with self.stats_index as _:
            result = _.summary_stats()

            assert type(result) is Schema__MGraph__Index__Stats__Summary
            assert result.total_nodes == 3
            assert result.total_predicates == 1

    # =========================================================================
    # Paths Stats Tests
    # =========================================================================

    def test_paths_stats__empty(self):
        with self.stats_index as _:
            result = _.paths_stats()

            assert type(result) is Schema__MGraph__Index__Stats__Paths
            assert result.node_paths == {}
            assert result.edge_paths == {}

    def test_paths_stats__with_paths(self):
        from mgraph_db.mgraph.schemas.identifiers.Node_Path import Node_Path
        from mgraph_db.mgraph.schemas.identifiers.Edge_Path import Edge_Path

        node_path = Node_Path('/test/path')
        edge_path = Edge_Path('/edge/path')

        self.paths_data.nodes_by_path[node_path] = {Node_Id(Obj_Id()), Node_Id(Obj_Id())}
        self.paths_data.edges_by_path[edge_path] = {Edge_Id(Obj_Id())}

        with self.stats_index as _:
            result = _.paths_stats()
            assert result.obj() == __(node_paths=__(_test_path=2),
                                      edge_paths=__(_edge_path=1))
            assert result.json() == {'edge_paths': {'/edge/path': 1},
                                     'node_paths': {'/test/path': 2}}
            assert '/test/path' in result.node_paths
            assert result.node_paths['/test/path'] == 2
            assert '/edge/path' in result.edge_paths
            assert result.edge_paths['/edge/path'] == 1

    # =========================================================================
    # Index Data Stats Tests
    # =========================================================================

    def test_index_data_stats(self):
        node_id_1 = Node_Id(Obj_Id())
        node_id_2 = Node_Id(Obj_Id())

        self.types_data.nodes_by_type['TestNode'] = {node_id_1, node_id_2}
        self.types_data.edges_by_type['TestEdge'] = {Edge_Id(Obj_Id())}
        self.edges_index.index_edge(Edge_Id(Obj_Id()), node_id_1, node_id_2)

        with self.stats_index as _:
            result = _.index_data_stats()

            assert type(result) is Schema__MGraph__Index__Stats__Index_Data
            assert result.edge_to_nodes == 1
            assert 'TestNode' in result.nodes_by_type
            assert result.nodes_by_type['TestNode'] == 2
            assert 'TestEdge' in result.edges_by_type