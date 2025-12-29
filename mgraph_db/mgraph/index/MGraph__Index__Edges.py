from typing                                                              import Set, Dict, Tuple, List, Optional
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                       import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Edges   import Schema__MGraph__Index__Data__Edges
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id        import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe


class MGraph__Index__Edges(Type_Safe):
    data: Schema__MGraph__Index__Data__Edges  = None                                             # Dedicated edges index data

    # =========================================================================
    # Node Edge Sets - Initialize
    # =========================================================================

    def init_node_edge_sets(self, node_id: Node_Id) -> None:                                 # Initialize empty edge sets for a node
        if node_id not in self.data.nodes_to_outgoing_edges:
            self.data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.data.nodes_to_incoming_edges:
            self.data.nodes_to_incoming_edges[node_id] = set()

    # =========================================================================
    # Edge-Node Mapping - Add Methods
    # =========================================================================

    def index_edge(self, edge_id     : Edge_Id ,                                             # Index an edge's node connections
                         from_node_id: Node_Id ,
                         to_node_id  : Node_Id ) -> None:

        self.data.edges_to_nodes[edge_id] = (from_node_id, to_node_id)                       # Store edge endpoints

        if from_node_id not in self.data.nodes_to_outgoing_edges:                            # Add to outgoing edges
            self.data.nodes_to_outgoing_edges[from_node_id] = set()
        self.data.nodes_to_outgoing_edges[from_node_id].add(edge_id)

        if to_node_id not in self.data.nodes_to_incoming_edges:                              # Add to incoming edges
            self.data.nodes_to_incoming_edges[to_node_id] = set()
        self.data.nodes_to_incoming_edges[to_node_id].add(edge_id)

    # =========================================================================
    # Edge-Node Mapping - Remove Methods
    # =========================================================================

    def remove_node_edge_sets(self, node_id: Node_Id) -> Tuple[Set[Edge_Id], Set[Edge_Id]]:  # Remove and return node's edge sets
        outgoing_edges = self.data.nodes_to_outgoing_edges.pop(node_id, set())
        incoming_edges = self.data.nodes_to_incoming_edges.pop(node_id, set())
        return outgoing_edges, incoming_edges

    def remove_edge(self, edge_id: Edge_Id) -> Optional[Tuple[Node_Id, Node_Id]]:            # Remove edge and return its endpoints
        if edge_id in self.data.edges_to_nodes:
            from_node_id, to_node_id = self.data.edges_to_nodes.pop(edge_id)
            self._remove_edge_from_node_sets(edge_id, from_node_id, to_node_id)
            return from_node_id, to_node_id
        return None

    def _remove_edge_from_node_sets(self, edge_id     : Edge_Id ,                            # Remove edge from node's edge sets
                                          from_node_id: Node_Id ,
                                          to_node_id  : Node_Id ) -> None:
        if from_node_id in self.data.nodes_to_outgoing_edges:
            self.data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
        if to_node_id in self.data.nodes_to_incoming_edges:
            self.data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

    # =========================================================================
    # Edge Query Methods
    # =========================================================================

    def get_edge_nodes(self, edge_id: Edge_Id) -> Optional[Tuple[Node_Id, Node_Id]]:         # Get edge endpoints (from, to)
        return self.data.edges_to_nodes.get(edge_id)

    def get_edge_from_node(self, edge_id: Edge_Id) -> Optional[Node_Id]:                     # Get edge source node
        result = self.data.edges_to_nodes.get(edge_id)
        return result[0] if result else None

    def get_edge_to_node(self, edge_id: Edge_Id) -> Optional[Node_Id]:                       # Get edge target node
        result = self.data.edges_to_nodes.get(edge_id)
        return result[1] if result else None

    def has_edge(self, edge_id: Edge_Id) -> bool:                                            # Check if edge exists
        return edge_id in self.data.edges_to_nodes

    def edge_count(self) -> int:                                                             # Get total edge count
        return len(self.data.edges_to_nodes)

    # =========================================================================
    # Node Edge Query Methods
    # =========================================================================

    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Edge_Id]:           # Get outgoing edges for a node
        return self.data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_id_outgoing_edges(self, node_id: Node_Id) -> Set[Edge_Id]:                  # Get outgoing edges by node ID
        return self.data.nodes_to_outgoing_edges.get(node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Edge_Id]:           # Get incoming edges for a node
        return self.data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_node_id_incoming_edges(self, node_id: Node_Id) -> Set[Edge_Id]:                  # Get incoming edges by node ID
        return self.data.nodes_to_incoming_edges.get(node_id, set())

    def get_node_all_edges(self, node_id: Node_Id) -> Set[Edge_Id]:                          # Get all edges connected to a node
        outgoing = self.data.nodes_to_outgoing_edges.get(node_id, set())
        incoming = self.data.nodes_to_incoming_edges.get(node_id, set())
        return outgoing | incoming

    def count_node_outgoing_edges(self, node_id: Node_Id) -> int:                            # Count outgoing edges
        return len(self.data.nodes_to_outgoing_edges.get(node_id, set()))

    def count_node_incoming_edges(self, node_id: Node_Id) -> int:                            # Count incoming edges
        return len(self.data.nodes_to_incoming_edges.get(node_id, set()))

    def has_node_outgoing_edges(self, node_id: Node_Id) -> bool:                             # Check if node has outgoing edges
        return bool(self.data.nodes_to_outgoing_edges.get(node_id))

    def has_node_incoming_edges(self, node_id: Node_Id) -> bool:                             # Check if node has incoming edges
        return bool(self.data.nodes_to_incoming_edges.get(node_id))

    # =========================================================================
    # Node Traversal Methods
    # =========================================================================

    def get_connected_nodes_outgoing(self, node_id: Node_Id) -> Set[Node_Id]:                # Get nodes connected via outgoing edges
        result = set()
        for edge_id in self.data.nodes_to_outgoing_edges.get(node_id, set()):
            edge_nodes = self.data.edges_to_nodes.get(edge_id)
            if edge_nodes:
                _, to_node_id = edge_nodes
                result.add(to_node_id)
        return result

    def get_connected_nodes_incoming(self, node_id: Node_Id) -> Set[Node_Id]:                # Get nodes connected via incoming edges
        result = set()
        for edge_id in self.data.nodes_to_incoming_edges.get(node_id, set()):
            edge_nodes = self.data.edges_to_nodes.get(edge_id)
            if edge_nodes:
                from_node_id, _ = edge_nodes
                result.add(from_node_id)
        return result

    def get_all_connected_nodes(self, node_id: Node_Id) -> Set[Node_Id]:                     # Get all connected nodes (both directions)
        return self.get_connected_nodes_outgoing(node_id) | self.get_connected_nodes_incoming(node_id)

    # =========================================================================
    # List-based accessors (for compatibility)
    # =========================================================================

    def edges_ids__from__node_id(self, node_id: Node_Id) -> List[Edge_Id]:                   # Get outgoing edge IDs as list
        return list(self.data.nodes_to_outgoing_edges.get(node_id, set()))

    def edges_ids__to__node_id(self, node_id: Node_Id) -> List[Edge_Id]:                     # Get incoming edge IDs as list
        return list(self.data.nodes_to_incoming_edges.get(node_id, set()))

    def nodes_ids__from__node_id(self, node_id: Node_Id) -> List[Node_Id]:                   # Get target node IDs via outgoing edges
        nodes_ids = []
        for edge_id in self.edges_ids__from__node_id(node_id):
            edge_nodes = self.data.edges_to_nodes.get(edge_id)
            if edge_nodes:
                _, to_node_id = edge_nodes
                nodes_ids.append(to_node_id)
        return nodes_ids

    def nodes_ids__to__node_id(self, node_id: Node_Id) -> List[Node_Id]:                     # Get source node IDs via incoming edges
        nodes_ids = []
        for edge_id in self.edges_ids__to__node_id(node_id):
            edge_nodes = self.data.edges_to_nodes.get(edge_id)
            if edge_nodes:
                from_node_id, _ = edge_nodes
                nodes_ids.append(from_node_id)
        return nodes_ids

    # =========================================================================
    # Raw Data Accessors
    # =========================================================================

    def edges_to_nodes(self) -> Dict[Edge_Id, Tuple[Node_Id, Node_Id]]:                      # Raw accessor
        return self.data.edges_to_nodes

    def nodes_to_outgoing_edges(self) -> Dict[Node_Id, Set[Edge_Id]]:                        # Raw accessor
        return self.data.nodes_to_outgoing_edges

    def nodes_to_incoming_edges(self) -> Dict[Node_Id, Set[Edge_Id]]:                        # Raw accessor
        return self.data.nodes_to_incoming_edges