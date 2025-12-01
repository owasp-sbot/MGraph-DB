from unittest                                                       import TestCase

from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
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

