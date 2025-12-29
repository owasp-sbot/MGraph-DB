from typing                                                              import Set, Optional, Dict
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                       import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                       import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Paths   import Schema__MGraph__Index__Data__Paths
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                      import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                      import Node_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id        import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe


class MGraph__Index__Paths(Type_Safe):
    data    : Schema__MGraph__Index__Data__Paths = None                                      # Dedicated paths index data
    enabled : bool = True


    # =========================================================================
    # Add Methods
    # =========================================================================

    def index_node_path(self, node: Schema__MGraph__Node) -> None:                           # Index a node's path if present
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if node.node_path:
            node_path = node.node_path
            if node_path not in self.data.nodes_by_path:
                self.data.nodes_by_path[node_path] = set()
            self.data.nodes_by_path[node_path].add(node.node_id)

    def index_edge_path(self, edge: Schema__MGraph__Edge) -> None:                           # Index an edge's path if present
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if edge.edge_path:
            edge_path = edge.edge_path
            if edge_path not in self.data.edges_by_path:
                self.data.edges_by_path[edge_path] = set()
            self.data.edges_by_path[edge_path].add(edge.edge_id)

    # =========================================================================
    # Remove Methods
    # =========================================================================

    def remove_node_path(self, node: Schema__MGraph__Node) -> None:                          # Remove a node's path from index if present
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if node.node_path:
            node_path = node.node_path
            if node_path in self.data.nodes_by_path:
                self.data.nodes_by_path[node_path].discard(node.node_id)
                if not self.data.nodes_by_path[node_path]:                                   # Clean up empty sets
                    del self.data.nodes_by_path[node_path]

    def remove_edge_path(self, edge: Schema__MGraph__Edge) -> None:                          # Remove an edge's path from index if present
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if edge.edge_path:
            edge_path = edge.edge_path
            if edge_path in self.data.edges_by_path:
                self.data.edges_by_path[edge_path].discard(edge.edge_id)
                if not self.data.edges_by_path[edge_path]:                                   # Clean up empty sets
                    del self.data.edges_by_path[edge_path]

    def remove_edge_path_by_id(self, edge_id: Edge_Id) -> None:                              # Remove edge path using only its ID
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        for path, edge_ids in list(self.data.edges_by_path.items()):
            if edge_id in edge_ids:
                edge_ids.discard(edge_id)
                if not edge_ids:
                    del self.data.edges_by_path[path]
                break

    # =========================================================================
    # Query Methods
    # =========================================================================

    def get_nodes_by_path(self, node_path: Node_Path) -> Set[Node_Id]:                       # Get all node IDs with a specific path
        return self.data.nodes_by_path.get(node_path, set())

    def get_edges_by_path(self, edge_path: Edge_Path) -> Set[Edge_Id]:                       # Get all edge IDs with a specific path
        return self.data.edges_by_path.get(edge_path, set())

    def get_all_node_paths(self) -> Set[Node_Path]:                                          # Get all unique node paths in graph
        return set(self.data.nodes_by_path.keys())

    def get_all_edge_paths(self) -> Set[Edge_Path]:                                          # Get all unique edge paths in graph
        return set(self.data.edges_by_path.keys())

    def get_node_path(self, node_id: Node_Id) -> Optional[Node_Path]:                        # Get path for a specific node
        for path, node_ids in self.data.nodes_by_path.items():
            if node_id in node_ids:
                return path
        return None

    def get_edge_path(self, edge_id: Edge_Id) -> Optional[Edge_Path]:                        # Get path for a specific edge
        for path, edge_ids in self.data.edges_by_path.items():
            if edge_id in edge_ids:
                return path
        return None

    def count_nodes_by_path(self, node_path: Node_Path) -> int:                              # Count nodes at a path
        return len(self.data.nodes_by_path.get(node_path, set()))

    def count_edges_by_path(self, edge_path: Edge_Path) -> int:                              # Count edges at a path
        return len(self.data.edges_by_path.get(edge_path, set()))

    def has_node_path(self, node_path: Node_Path) -> bool:                                   # Check if node path exists
        return node_path in self.data.nodes_by_path

    def has_edge_path(self, edge_path: Edge_Path) -> bool:                                   # Check if edge path exists
        return edge_path in self.data.edges_by_path

    # =========================================================================
    # Raw Data Accessors
    # =========================================================================

    def nodes_by_path(self) -> Dict[Node_Path, Set[Node_Id]]:                                # Raw accessor for nodes_by_path
        return self.data.nodes_by_path

    def edges_by_path(self) -> Dict[Edge_Path, Set[Edge_Id]]:                                # Raw accessor for edges_by_path
        return self.data.edges_by_path