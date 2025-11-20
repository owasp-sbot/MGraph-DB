from typing                                                         import List, Type
from mgraph_db.mgraph.domain.Domain__MGraph__Types                  import Domain__MGraph__Types
from mgraph_db.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Domain__MGraph__Graph(Type_Safe):
    domain_types : Domain__MGraph__Types
    model        : Model__MGraph__Graph
    graph_type   : Type['Domain__MGraph__Graph']


    def delete_edge(self, edge_id: Obj_Id) -> bool:
        return self.model.delete_edge(edge_id)

    def delete_node(self, node_id: Obj_Id) -> bool:
        return self.model.delete_node(node_id)

    def edge(self, edge_id: Obj_Id) -> Domain__MGraph__Edge:
        edge = self.model.edge(edge_id)
        if edge:
            return self.mgraph_edge(edge=edge)

    def edges(self) -> List[Domain__MGraph__Edge]:
        return [self.mgraph_edge(edge=edge) for edge in self.model.edges()]

    def edges_ids(self):
        return self.model.edges_ids()

    def graph_id(self):
        return self.model.data.graph_id

    def mgraph_edge(self, edge: Model__MGraph__Edge) -> Domain__MGraph__Edge:
        return self.domain_types.edge_domain_type(edge=edge, graph=self.model)

    def mgraph_node(self, node: Model__MGraph__Node) -> Domain__MGraph__Edge:
        return self.domain_types.node_domain_type(node=node, graph=self.model)

    def add_edge(self, edge: Schema__MGraph__Edge):
        edge = self.model.add_edge(edge)
        return self.mgraph_edge(edge=edge)

    def connect_nodes(self, from_node: Domain__MGraph__Node,
                            to_node  : Domain__MGraph__Node,
                            edge_type: Type[Schema__MGraph__Edge] = None
                       ) -> Domain__MGraph__Edge:                   # Creates an edge between two nodes
        return self.new_edge(edge_type    = edge_type ,
                             from_node_id = from_node.node_id,
                             to_node_id   = to_node.node_id  )

    def new_edge(self, **kwargs) -> Domain__MGraph__Edge:
        edge = self.model.new_edge(**kwargs)
        return self.mgraph_edge(edge=edge)

    def add_node(self, node: Schema__MGraph__Node):
        node = self.model.add_node(node)
        return self.mgraph_node(node=node)

    def new_node(self, **kwargs)-> Domain__MGraph__Node:
        node = self.model.new_node(**kwargs)
        return self.mgraph_node(node=node)

    # todo: check this logic to if we need to create new objects every time this is called
    def node(self, node_id: Obj_Id) -> Domain__MGraph__Node:
        node = self.model.node(node_id)
        if node:
            return self.mgraph_node(node=node)

    def nodes(self) -> List[Domain__MGraph__Node]:
        return [self.mgraph_node(node=node) for node in self.model.nodes()]

    def nodes_ids(self):
        return self.model.nodes_ids()

