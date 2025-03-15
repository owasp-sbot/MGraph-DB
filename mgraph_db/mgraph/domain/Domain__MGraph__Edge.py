from mgraph_db.mgraph.domain.Domain__MGraph__Node          import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Label  import Schema__MGraph__Edge__Label
from osbot_utils.helpers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.Type_Safe                       import Type_Safe
from osbot_utils.type_safe.methods.type_safe_property      import set_as_property


class Domain__MGraph__Edge(Type_Safe):                                                                  # Domain class for edges
    edge : Model__MGraph__Edge                                                                          # Reference to edge model
    graph: Model__MGraph__Graph                                                                         # Reference to graph model

    edge_id     = set_as_property('edge.data', 'edge_id'    , Obj_Id                     ) # Edge ID
    edge_label  = set_as_property('edge.data', 'edge_label' , Schema__MGraph__Edge__Label)
    edge_type   = set_as_property('edge.data', 'edge_type'  , type   )


    def from_node(self, domain_node_type = Domain__MGraph__Node) -> Domain__MGraph__Node:                                                        # Get source node
        node = self.graph.node(self.edge.from_node_id())
        if node:
            return domain_node_type(node=node, graph=self.graph)

    def from_node_id(self) -> Obj_Id:                                                              # Get source node ID
        return self.edge.from_node_id()

    def to_node(self, domain_node_type = Domain__MGraph__Node) -> Domain__MGraph__Node:                                                          # Get target node
        node = self.graph.node(self.edge.to_node_id())
        if node:
            return domain_node_type(node=node, graph=self.graph)

    def to_node_id(self) -> Obj_Id:                                                              # Get source node ID
        return self.edge.to_node_id()
