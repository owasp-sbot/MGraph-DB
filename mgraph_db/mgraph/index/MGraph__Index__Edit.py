from mgraph_db.mgraph.index.MGraph__Index__Edges                     import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                    import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Paths                     import MGraph__Index__Paths
from mgraph_db.mgraph.index.MGraph__Index__Types                     import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                    import MGraph__Index__Values
from mgraph_db.mgraph.actions.MGraph__Type__Resolver                 import MGraph__Type__Resolver
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                   import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                   import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value            import Schema__MGraph__Node__Value
from osbot_utils.helpers.timestamp_capture.decorators.timestamp      import timestamp
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id    import Edge_Id
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe


class MGraph__Index__Edit(Type_Safe):
    edges_index  : MGraph__Index__Edges      = None                                         # Edge-node relationships
    labels_index : MGraph__Index__Labels     = None                                         # Edge labels
    paths_index  : MGraph__Index__Paths      = None                                         # Node/edge paths
    types_index  : MGraph__Index__Types      = None                                         # Node/edge types
    values_index : MGraph__Index__Values     = None                                         # Value lookups
    resolver     : MGraph__Type__Resolver    = None                                         # Type resolution

    # =========================================================================
    # Node Operations
    # =========================================================================

    #@timestamp(name='add_node (index)')
    def add_node(self, node: Schema__MGraph__Node) -> None:
        node_id        = node.node_id
        node_type      = self.resolver.node_type(node.node_type)
        node_type_name = node_type.__name__

        self.edges_index.init_node_edge_sets(node_id)
        self.types_index.index_node_type(node_id, node_type_name)
        self.paths_index.index_node_path(node)

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):
            self.values_index.add_value_node(node)

    def remove_node(self, node: Schema__MGraph__Node) -> None:
        node_id = node.node_id

        outgoing_edges, incoming_edges = self.edges_index.remove_node_edge_sets(node_id)

        for edge_id in outgoing_edges | incoming_edges:                                      # Remove all connected edges
            self.remove_edge_by_id(edge_id)

        node_type      = self.resolver.node_type(node.node_type)
        node_type_name = node_type.__name__

        self.types_index.remove_node_type(node_id, node_type_name)
        self.paths_index.remove_node_path(node)

        if node.node_type and issubclass(node.node_type, Schema__MGraph__Node__Value):
            self.values_index.remove_value_node(node)

    # =========================================================================
    # Edge Operations
    # =========================================================================

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:
        edge_id        = edge.edge_id
        from_node_id   = edge.from_node_id
        to_node_id     = edge.to_node_id
        edge_type      = self.resolver.edge_type(edge.edge_type)
        edge_type_name = edge_type.__name__

        self.edges_index.index_edge(edge_id, from_node_id, to_node_id)
        self.labels_index.add_edge_label(edge)
        self.types_index.index_edge_type(edge_id, from_node_id, to_node_id, edge_type_name)
        self.paths_index.index_edge_path(edge)

    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:
        self.remove_edge_by_id(edge.edge_id)

    def remove_edge_by_id(self, edge_id: Edge_Id) -> None:
        edge_type_name = self.types_index.data.edges_types.pop(edge_id, None)                # Get type before removing

        edge_nodes = self.edges_index.remove_edge(edge_id)
        if edge_nodes:
            from_node_id, to_node_id = edge_nodes
            self.types_index.remove_edge_type_by_node(edge_id, from_node_id, to_node_id, edge_type_name)

        self.types_index.remove_edge_type(edge_id, edge_type_name)
        self.paths_index.remove_edge_path_by_id(edge_id)
        self.labels_index.remove_edge_label_by_id(edge_id)