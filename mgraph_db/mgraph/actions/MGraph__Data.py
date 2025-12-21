from typing                                                         import List
from osbot_utils.type_safe.type_safe_core.decorators.type_safe      import type_safe
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class MGraph__Data(Type_Safe):
    graph: Domain__MGraph__Graph


    def edge(self, edge_id: Edge_Id) -> Domain__MGraph__Edge:                                                               # Get an edge by its ID
        return self.graph.edge(edge_id)

    #todo: refactor to use self.index()
    def edges(self) -> List[Domain__MGraph__Edge]:                                                                              # Get all edges in the graph
        return self.graph.edges()

    # todo: refactor to use self.index()
    def edges_ids(self):
        return list(self.graph.edges_ids())

    def graph_id(self):
        return self.graph.graph_id()

    # def index(self):
    #     return MGraph__Index.from_graph(graph=self.graph)

    @type_safe
    def node(self, node_id: Node_Id) -> Domain__MGraph__Node:                                                               # Get a node by its ID
        return self.graph.node(node_id)

    # todo: refactor to use self.index()
    def nodes(self) -> List[Domain__MGraph__Node]:                                                                              # Get all nodes in the graph
        return self.graph.nodes()

    def nodes_ids(self):
        return list(self.graph.nodes_ids())

    def stats(self):
        return dict(nodes_ids = len(self.nodes_ids()),
                    edges_ids = len(self.edges_ids()))
