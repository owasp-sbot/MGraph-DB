from typing                                                         import Type
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.actions.MGraph__Data                          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Index                         import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class MGraph__Edit(Type_Safe):
    graph    : Domain__MGraph__Graph
    data_type: Type[MGraph__Data]

    def add_node(self, node: Schema__MGraph__Node):
        with self.index() as index:                                     # used context here so that we have an index object in the state before we add a node (or the node data will be loaded twice)
            result = self.graph.add_node(node)                          # Add node to graph
            index.add_node(node)                                        # Add to index
        return result

    def add_edge(self, edge: Schema__MGraph__Edge):
        result = self.graph.add_edge(edge)                               # Add edge to graph
        self.index().add_edge(edge)                                      # Add to index
        return result

    def create_edge(self):
        node_1 = self.new_node()
        node_2 = self.new_node()
        edge_1 = self.connect_nodes(node_1, node_2)
        return dict(node_1 = node_1,
                    node_2 = node_2,
                    edge_1 = edge_1)

    def connect_nodes(self, from_node: Domain__MGraph__Node,
                            to_node  : Domain__MGraph__Node,
                            edge_type: Type[Schema__MGraph__Edge] = None
                       ) -> Domain__MGraph__Edge:
        edge_domain = self.graph.connect_nodes(from_node=from_node, to_node=to_node, edge_type=edge_type)
        edge_model  = edge_domain.edge
        edge_schema = edge_model.data
        self.index().add_edge(edge_schema)
        return edge_domain


    def get_or_create_edge(self, from_node_id : Node_Id                          ,
                                 to_node_id   : Node_Id                          ,
                                 edge_type    : Type[Schema__MGraph__Edge] = None,               # Get existing edge or create new one
                                 predicate    : str = None                                           # Optional predicate to match
                            ) -> Domain__MGraph__Edge:


        if edge_type is None:                                                                                           # If edge_type is None, use the default Schema__MGraph__Edge
            edge_type = Schema__MGraph__Edge

        edge_type_name = edge_type.__name__

        with self.index() as index:

            existing_edges = index.nodes_to_outgoing_edges_by_type().get(from_node_id, {}).get(edge_type_name, set())   # Get all outgoing edges of the specified type from the source node


            if predicate is not None:                                                                                   # First, try to find an exact match (same edge_type, endpoints, and predicate)
                for edge_id in existing_edges:
                    if index.edges_to_nodes().get(edge_id)[1] == to_node_id:                                            # Check if the edge has the same predicate
                        edge = self.data().edge(edge_id)
                        if edge:
                            if edge.edge.data.edge_label:
                                if edge.edge.data.edge_label.predicate == predicate:
                                    return edge


            for edge_id in existing_edges:                                                                              # If no match with predicate or predicate is None, check just for edge_type and endpoints
                if index.edges_to_nodes().get(edge_id)[1] == to_node_id:
                    # If predicate was specified, but we're here, it means no edge had the matching predicate
                    # If predicate was not specified, we return the first edge with matching endpoints and type
                    if predicate is None:
                        return self.data().edge(edge_id)

            return self.new_edge(edge_type    = edge_type    ,                                                          # Create new edge if none exists with matching criteria
                                 from_node_id = from_node_id ,
                                 to_node_id   = to_node_id   )

    def new_node(self, **kwargs):
        with self.index() as index:
            node = self.graph.new_node(**kwargs)                             # Create new node
            index.add_node(node.node.data)                           # Add to index
        return node

    def new_edge(self, **kwargs) -> Domain__MGraph__Edge:                # Add a new edge between nodes
        edge = self.graph.new_edge(**kwargs)                             # Create new edge
        self.index().add_edge(edge.edge.data)                           # Add to index
        return edge

    def new_value(self, value,
                        key                                          = None,
                        node_type: Type[Schema__MGraph__Node__Value] = None):                               # get or create value (since the values have to be unique)
        node_id = self.index().values_index.get_node_id_by_value(value_type=type(value), value=str(value), key=key, node_type=node_type)  # First try to find existing value node
        if node_id:
            return self.data().node(node_id)
        if node_type is None:
            node_type= Schema__MGraph__Node__Value
        return self.new_node(node_type=node_type, value_type=type(value), value=str(value), key=key)

    def delete_node(self, node_id: Node_Id) -> bool:                      # Remove a node and its connected edges
        node = self.data().node(node_id)
        if node:
            self.index().remove_node(node.node.data)                     # Remove from index first
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Edge_Id) -> bool:                      # Remove an edge
        edge = self.data().edge(edge_id)
        if edge:
            self.index().remove_edge(edge.edge.data)                     # Remove from index first
        return self.graph.delete_edge(edge_id)

    @cache_on_self
    def data(self):
        return self.data_type(graph=self.graph)

    @cache_on_self
    def index(self) -> MGraph__Index:                                    # Cached access to index
        return MGraph__Index.from_graph(self.graph)