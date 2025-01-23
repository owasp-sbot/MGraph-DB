from typing                                         import List
from mgraph_ai.mgraph.domain.Domain__MGraph__Edge   import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from mgraph_ai.mgraph.domain.Domain__MGraph__Node   import Domain__MGraph__Node
from osbot_utils.helpers.Obj_Id import Obj_Id
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class MGraph__Data(Type_Safe):
    graph: Domain__MGraph__Graph


    def edge(self, edge_id: Obj_Id) -> Domain__MGraph__Edge:                                                               # Get an edge by its ID
        return self.graph.edge(edge_id)

    def edges(self) -> List[Domain__MGraph__Edge]:                                                                              # Get all edges in the graph
        return self.graph.edges()

    def edges_ids(self):
        return list(self.graph.edges_ids())

    def graph_id(self):
        return self.graph.graph_id()


    def node(self, node_id: Obj_Id) -> Domain__MGraph__Node:                                                               # Get a node by its ID
        return self.graph.node(node_id)

    def nodes(self) -> List[Domain__MGraph__Node]:                                                                              # Get all nodes in the graph
        return self.graph.nodes()

    def nodes_ids(self):
        return list(self.graph.nodes_ids())
