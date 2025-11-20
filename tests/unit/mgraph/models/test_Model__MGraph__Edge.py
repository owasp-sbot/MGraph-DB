from unittest                                                    import TestCase
from mgraph_db.mgraph.models.Model__MGraph__Edge                 import Model__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge               import Schema__MGraph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id



class test_Model__MGraph__Edge(TestCase):

    def setUp(self):    # Initialize test data
        self.from_node_id = Obj_Id()
        self.to_node_id   = Obj_Id()
        self.edge = Schema__MGraph__Edge( edge_type    = Schema__MGraph__Edge,
                                          from_node_id = self.from_node_id   ,
                                          to_node_id   = self.to_node_id     )
        self.model = Model__MGraph__Edge(data=self.edge)

    def test_init(self):    # Tests basic initialization
        assert type(self.model)          is Model__MGraph__Edge
        assert self.model.data           is self.edge
        assert self.model.from_node_id() == self.from_node_id
        assert self.model.to_node_id()   == self.to_node_id

    def test_node_ids(self):    # Tests node ID getters
        assert self.model.from_node_id() == self.from_node_id
        assert self.model.to_node_id()   == self.to_node_id