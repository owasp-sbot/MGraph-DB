from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from osbot_utils.helpers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.Type_Safe                       import Type_Safe


class Model__MGraph__Edge(Type_Safe):
    data: Schema__MGraph__Edge

    def from_node_id(self) -> Obj_Id:
        return self.data.from_node_id

    def edge_config(self) -> Schema__MGraph__Edge__Config:
        return self.data.edge_config

    def edge_id(self) -> Obj_Id:
        return self.edge_config().edge_id

    def to_node_id(self) -> Obj_Id:
        return self.data.to_node_id