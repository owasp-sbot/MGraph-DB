from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                import Schema__MGraph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.Type_Safe                              import Type_Safe


class Model__MGraph__Edge(Type_Safe):
    data: Schema__MGraph__Edge

    def from_node_id(self) -> Node_Id:
        return self.data.from_node_id

    def edge_id(self) -> Edge_Id:
        return self.data.edge_id

    def to_node_id(self) -> Node_Id:
        return self.data.to_node_id