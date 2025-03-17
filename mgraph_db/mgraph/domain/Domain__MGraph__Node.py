from typing                                           import List
from mgraph_db.mgraph.models.Model__MGraph__Graph     import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node      import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Edge      import Model__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                  import Type_Safe
from osbot_utils.type_safe.methods.type_safe_property import set_as_property

class Domain__MGraph__Node(Type_Safe):                                                       # Domain class for nodes
    node : Model__MGraph__Node                                                              # Reference to node model
    graph: Model__MGraph__Graph                                                             # Reference to graph model

    node_data = set_as_property('node.data' , 'node_data')                                  # Node configuration property
    node_id   = set_as_property('node.data' , 'node_id'  )                                  # Node ID property
    node_type = set_as_property('node.data' , 'node_type')                                  # Note Type property
    graph_id  = set_as_property('graph.data', 'graph_id' )                                  # Graph ID property

    def add_node(self, node: Model__MGraph__Node) -> None:                                  # Add a node to the graph
        self.graph.add_node(node.data)

    # todo: refactor to not use self.graph.edges()
    def models__edges(self) -> List[Model__MGraph__Edge]:                                  # Get all model edges connected to this node
        connected_edges = []
        for edge in self.graph.edges():
            if edge.from_node_id() == self.node_id or edge.to_node_id() == self.node_id:
                connected_edges.append(edge)
        return connected_edges

    # todo: this needed to be refactored to the MGraph_Index (since this is transversing all of self.graph.edges() to find an edge)
    def models__from_edges(self) -> List[Model__MGraph__Edge]:                             # Get model edges where this node is the source
        outgoing_edges = []
        for edge in self.graph.edges():
            if edge.from_node_id() == self.node_id:
                outgoing_edges.append(edge)
        return outgoing_edges

    # todo: refactor to not use self.graph.edges()
    def models__to_edges(self) -> List[Model__MGraph__Edge]:                               # Get model edges where this node is the target
        incoming_edges = []
        for edge in self.graph.edges():
            if edge.to_node_id() == self.node_id:
                incoming_edges.append(edge)
        return incoming_edges

    def model__node_from_edge(self, edge: Model__MGraph__Edge) -> [Model__MGraph__Node]:  # Get connected node from edge
        if edge.from_node_id() == self.node_id:
            return self.graph.node(edge.to_node_id())
        if edge.to_node_id() == self.node_id:
            return self.graph.node(edge.from_node_id())
        return None

    def value(self):
        return self.node_data.value