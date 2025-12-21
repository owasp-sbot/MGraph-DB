from unittest                                                            import TestCase
from mgraph_db.mgraph.index.MGraph__Index__Edges                         import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                        import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Types                         import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                        import MGraph__Index__Values
from mgraph_db.mgraph.index.MGraph__Index__Query                         import MGraph__Index__Query
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Edges   import Schema__MGraph__Index__Data__Edges
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Labels  import Schema__MGraph__Index__Data__Labels
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Types   import Schema__MGraph__Index__Data__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id        import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id        import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id         import Obj_Id


class test_MGraph__Index__Query(TestCase):

    def setUp(self):
        self.edges_data   = Schema__MGraph__Index__Data__Edges()
        self.labels_data  = Schema__MGraph__Index__Data__Labels()
        self.types_data   = Schema__MGraph__Index__Data__Types()
        self.edges_index  = MGraph__Index__Edges (data=self.edges_data )
        self.labels_index = MGraph__Index__Labels(data=self.labels_data)
        self.types_index  = MGraph__Index__Types (data=self.types_data )
        self.values_index = MGraph__Index__Values()
        self.query_index  = MGraph__Index__Query(edges_index  = self.edges_index  ,
                                                  labels_index = self.labels_index ,
                                                  types_index  = self.types_index  ,
                                                  values_index = self.values_index )

    def test__init__(self):
        with self.query_index as _:
            assert type(_)              is MGraph__Index__Query
            assert type(_.edges_index)  is MGraph__Index__Edges
            assert type(_.labels_index) is MGraph__Index__Labels
            assert type(_.types_index)  is MGraph__Index__Types
            assert type(_.values_index) is MGraph__Index__Values

    # =========================================================================
    # Node Connection Query Tests
    # =========================================================================

    def test_get_node_connected_to_node__outgoing(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        edge_type = 'TestEdge'

        self.edges_index.index_edge(edge_id, node_a, node_b)
        self.types_index.index_edge_type(edge_id, node_a, node_b, edge_type)

        with self.query_index as _:
            result = _.get_node_connected_to_node__outgoing(node_a, edge_type)

            assert result == node_b

    def test_get_node_connected_to_node__outgoing__not_found(self):
        with self.query_index as _:
            result = _.get_node_connected_to_node__outgoing(Node_Id(Obj_Id()), 'NonExistent')

            assert result is None

    def test_get_node_connected_to_node__incoming(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        edge_type = 'TestEdge'

        self.edges_index.index_edge(edge_id, node_a, node_b)
        self.types_index.index_edge_type(edge_id, node_a, node_b, edge_type)

        with self.query_index as _:
            result_1 = _.get_node_connected_to_node__incoming(node_b, edge_type)

            assert result_1 == node_a

            result_2 = _.get_node_connected_to_node__incoming(node_b, '')
            assert result_2 is None

    # =========================================================================
    # Predicate-Based Query Tests
    # =========================================================================

    def test_get_node_outgoing_edges_by_predicate(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        predicate = Safe_Id('knows')

        self.edges_index.index_edge(edge_id, node_a, node_b)
        self.labels_data.edges_predicates[edge_id] = predicate
        self.labels_data.edges_by_predicate[predicate] = {edge_id}

        with self.query_index as _:
            result = _.get_node_outgoing_edges_by_predicate(node_a, predicate)

            assert edge_id in result

    def test_get_node_outgoing_edges_by_predicate__empty(self):
        with self.query_index as _:
            result = _.get_node_outgoing_edges_by_predicate(Node_Id(Obj_Id()), Safe_Id('unknown'))

            assert result == set()

    def test_get_node_incoming_edges_by_predicate(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        edge_id   = Edge_Id(Obj_Id())
        predicate = Safe_Id('knows')

        self.edges_index.index_edge(edge_id, node_a, node_b)
        self.labels_data.edges_predicates[edge_id] = predicate
        self.labels_data.edges_by_predicate[predicate] = {edge_id}

        with self.query_index as _:
            result = _.get_node_incoming_edges_by_predicate(node_b, predicate)

            assert edge_id in result

    def test_get_nodes_by_predicate(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        node_c    = Node_Id(Obj_Id())
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        predicate = Safe_Id('knows')

        self.edges_index.index_edge(edge_id_1, node_a, node_b)
        self.edges_index.index_edge(edge_id_2, node_a, node_c)
        self.labels_data.edges_predicates[edge_id_1] = predicate
        self.labels_data.edges_predicates[edge_id_2] = predicate
        self.labels_data.edges_by_predicate[predicate] = {edge_id_1, edge_id_2}

        with self.query_index as _:
            result = _.get_nodes_by_predicate(node_a, predicate)

            assert node_b in result
            assert node_c in result
            assert len(result) == 2

    def test_get_nodes_by_incoming_predicate(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        node_c    = Node_Id(Obj_Id())
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        predicate = Safe_Id('likes')

        self.edges_index.index_edge(edge_id_1, node_a, node_c)
        self.edges_index.index_edge(edge_id_2, node_b, node_c)
        self.labels_data.edges_predicates[edge_id_1] = predicate
        self.labels_data.edges_predicates[edge_id_2] = predicate
        self.labels_data.edges_by_predicate[predicate] = {edge_id_1, edge_id_2}

        with self.query_index as _:
            result = _.get_nodes_by_incoming_predicate(node_c, predicate)

            assert node_a in result
            assert node_b in result
            assert len(result) == 2

    # =========================================================================
    # Type-Based Query Tests
    # =========================================================================

    def test_get_nodes_by_outgoing_edge_type(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        node_c    = Node_Id(Obj_Id())
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        edge_type = 'FriendOf'

        self.edges_index.index_edge(edge_id_1, node_a, node_b)
        self.edges_index.index_edge(edge_id_2, node_a, node_c)
        self.types_index.index_edge_type(edge_id_1, node_a, node_b, edge_type)
        self.types_index.index_edge_type(edge_id_2, node_a, node_c, edge_type)

        with self.query_index as _:
            result = _.get_nodes_by_outgoing_edge_type(node_a, edge_type)

            assert node_b in result
            assert node_c in result
            assert len(result) == 2

    def test_get_nodes_by_incoming_edge_type(self):
        node_a    = Node_Id(Obj_Id())
        node_b    = Node_Id(Obj_Id())
        node_c    = Node_Id(Obj_Id())
        edge_id_1 = Edge_Id(Obj_Id())
        edge_id_2 = Edge_Id(Obj_Id())
        edge_type = 'FriendOf'

        self.edges_index.index_edge(edge_id_1, node_a, node_c)
        self.edges_index.index_edge(edge_id_2, node_b, node_c)
        self.types_index.index_edge_type(edge_id_1, node_a, node_c, edge_type)
        self.types_index.index_edge_type(edge_id_2, node_b, node_c, edge_type)

        with self.query_index as _:
            result = _.get_nodes_by_incoming_edge_type(node_c, edge_type)

            assert node_a in result
            assert node_b in result
            assert len(result) == 2

    def test_get_nodes_by_outgoing_edge_type__empty(self):
        with self.query_index as _:
            result = _.get_nodes_by_outgoing_edge_type(Node_Id(Obj_Id()), 'NonExistent')

            assert result == set()