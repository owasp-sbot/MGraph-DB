from mgraph_db.mgraph.actions.MGraph__Data                       import MGraph__Data
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph


class MGraph__Json__Data(MGraph__Data):
    graph : Domain__MGraph__Json__Graph
    def root_node(self):
        return self.graph.root()

    def root_node_id(self):
        return self.root_node().node_id

    def root_property_id(self):
        root_id = self.root_node_id()                                           # get the MGraph__Json root id value
        nodes_ids = [edge.to_node_id() for edge in self.graph.edges()
                     if edge.from_node_id() == root_id]                         # get the nodes that it connects to
        if len(nodes_ids) == 1:                                                 # in a MGraph_Json there should only be one root property
            return nodes_ids[0]                                                 # return it
        return None

    def root_property_node(self):
        root_property_id = self.root_property_id()
        if root_property_id:
            return self.graph.node(root_property_id)