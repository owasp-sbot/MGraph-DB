from unittest                                                       import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data            import Schema__MGraph__Edge__Data
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge

class test_Schema__MGraph__Edge(TestCase):

    def setUp(self):    # Initialize test data
        self.from_node_id = Node_Id(Obj_Id())
        self.to_node_id   = Node_Id(Obj_Id())
        self.edge        = Schema__MGraph__Edge         ( edge_type    = Schema__MGraph__Edge   ,
                                                          from_node_id = self.from_node_id      ,
                                                          to_node_id   = self.to_node_id        )

    def test_init(self):                                                                # Tests basic initialization and type checking
        assert type(self.edge)                                 is Schema__MGraph__Edge
        assert self.edge.from_node_id                          == self.from_node_id
        assert self.edge.to_node_id                            == self.to_node_id


    def test_edge_with_path(self):                                                                  # Test edge creation with path
        node_id_1 = Node_Id()
        node_id_2 = Node_Id()

        with Schema__MGraph__Edge( edge_id      = Edge_Id()                         ,
                                   edge_type    = Schema__MGraph__Edge              ,
                                   edge_data    = Schema__MGraph__Edge__Data()      ,
                                   from_node_id = node_id_1                         ,
                                   to_node_id   = node_id_2                         ,
                                   edge_path    = Edge_Path("relationship.contains")) as _:
            assert _.edge_path      == Edge_Path("relationship.contains")
            assert str(_.edge_path) == "relationship.contains"

    def test_edge_without_path(self):                                                               # Test edge creation without path (backward compatibility)
        node_id_1 = Node_Id()
        node_id_2 = Node_Id()

        with Schema__MGraph__Edge( edge_id      = Edge_Id()                    ,
                                   edge_type    = Schema__MGraph__Edge         ,
                                   edge_data    = Schema__MGraph__Edge__Data() ,
                                   from_node_id = node_id_1                    ,
                                   to_node_id   = node_id_2                    ) as _:
            assert _.edge_path is None

    def test_edge_serialization_roundtrip_with_path(self):                                          # Test that edge path survives serialization
        node_id_1 = Node_Id()
        node_id_2 = Node_Id()

        with Schema__MGraph__Edge( edge_id      = Edge_Id()                    ,
                                   edge_type    = Schema__MGraph__Edge         ,
                                   edge_data    = Schema__MGraph__Edge__Data() ,
                                   from_node_id = node_id_1                    ,
                                   to_node_id   = node_id_2                    ,
                                   edge_path    = Edge_Path("test.edge.path")  ) as _:
            json_data = _.json()
            restored  = Schema__MGraph__Edge.from_json(json_data)

            assert restored.edge_path      == _.edge_path
            assert str(restored.edge_path) == "test.edge.path"