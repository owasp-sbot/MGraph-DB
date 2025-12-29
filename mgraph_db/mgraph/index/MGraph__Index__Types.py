from typing                                                              import Type, Set, Dict, Optional
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                       import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                       import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.index.Schema__MGraph__Index__Data__Types   import Schema__MGraph__Index__Data__Types
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id        import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id        import Node_Id
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe


class MGraph__Index__Types(Type_Safe):
    data    : Schema__MGraph__Index__Data__Types = None                                      # Dedicated types index data
    enabled : bool = True


    # =========================================================================
    # Node Type - Add Methods
    # =========================================================================

    def index_node_type(self, node_id: Node_Id, node_type_name: str) -> None:                # Index a node's type
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        self.data.nodes_types[node_id] = node_type_name                                      # Store node_id to type mapping

        if node_type_name not in self.data.nodes_by_type:                                    # Store type to node_ids mapping
            self.data.nodes_by_type[node_type_name] = set()
        self.data.nodes_by_type[node_type_name].add(node_id)

    # =========================================================================
    # Node Type - Remove Methods
    # =========================================================================

    def remove_node_type(self, node_id: Node_Id, node_type_name: str) -> None:               # Remove a node's type from index
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        if node_id in self.data.nodes_types:                                                 # Remove from nodes_types mapping
            del self.data.nodes_types[node_id]

        if node_type_name in self.data.nodes_by_type:                                        # Remove from nodes_by_type mapping
            self.data.nodes_by_type[node_type_name].discard(node_id)
            if not self.data.nodes_by_type[node_type_name]:                                  # Clean up empty sets
                del self.data.nodes_by_type[node_type_name]

    # =========================================================================
    # Edge Type - Add Methods
    # =========================================================================

    def index_edge_type(self, edge_id     : Edge_Id ,                                        # Index an edge's type
                              from_node_id: Node_Id ,
                              to_node_id  : Node_Id ,
                              edge_type_name: str   ) -> None:
        if not self.enabled:                                                                 # Skip if indexing disabled
            return
        self.data.edges_types[edge_id] = edge_type_name                                      # Store edge_id to type mapping

        if edge_type_name not in self.data.edges_by_type:                                    # Store type to edge_ids mapping
            self.data.edges_by_type[edge_type_name] = set()
        self.data.edges_by_type[edge_type_name].add(edge_id)

        self._index_edge_type_by_node(to_node_id  , edge_id, edge_type_name, incoming=True ) # Index by destination node (incoming)
        self._index_edge_type_by_node(from_node_id, edge_id, edge_type_name, incoming=False) # Index by source node (outgoing)

    def _index_edge_type_by_node(self, node_id       : Node_Id ,                             # Helper to index edge type by node
                                       edge_id       : Edge_Id ,
                                       edge_type_name: str     ,
                                       incoming      : bool    ) -> None:
        if incoming:
            edges_by_type = self.data.nodes_to_incoming_edges_by_type
        else:
            edges_by_type = self.data.nodes_to_outgoing_edges_by_type

        if node_id not in edges_by_type:
            edges_by_type[node_id] = {}
        if edge_type_name not in edges_by_type[node_id]:
            edges_by_type[node_id][edge_type_name] = set()
        edges_by_type[node_id][edge_type_name].add(edge_id)

    # =========================================================================
    # Edge Type - Remove Methods
    # =========================================================================

    def remove_edge_type(self, edge_id: Edge_Id, edge_type_name: str) -> None:               # Remove an edge's type from edges_by_type
        if edge_type_name and edge_type_name in self.data.edges_by_type:
            self.data.edges_by_type[edge_type_name].discard(edge_id)
            if not self.data.edges_by_type[edge_type_name]:                                  # Clean up empty sets
                del self.data.edges_by_type[edge_type_name]

    def remove_edge_type_by_node(self, edge_id       : Edge_Id ,                             # Remove edge type references from node mappings
                                       from_node_id  : Node_Id ,
                                       to_node_id    : Node_Id ,
                                       edge_type_name: str     ) -> None:
        self._remove_edge_type_from_node(from_node_id, edge_id, edge_type_name, incoming=False)
        self._remove_edge_type_from_node(to_node_id  , edge_id, edge_type_name, incoming=True )

    def _remove_edge_type_from_node(self, node_id       : Node_Id ,                          # Helper to remove edge type from node mapping
                                          edge_id       : Edge_Id ,
                                          edge_type_name: str     ,
                                          incoming      : bool    ) -> None:
        if incoming:
            edges_by_type = self.data.nodes_to_incoming_edges_by_type
        else:
            edges_by_type = self.data.nodes_to_outgoing_edges_by_type

        if edge_type_name and node_id in edges_by_type:
            if edge_type_name in edges_by_type[node_id]:
                edges_by_type[node_id][edge_type_name].discard(edge_id)
                if not edges_by_type[node_id][edge_type_name]:                               # Clean up empty type set
                    del edges_by_type[node_id][edge_type_name]
            if not edges_by_type[node_id]:                                                   # Clean up empty node entry
                del edges_by_type[node_id]

    # =========================================================================
    # Node Type - Query Methods
    # =========================================================================

    def get_node_type(self, node_id: Node_Id) -> Optional[str]:                              # Get type name for a specific node
        return self.data.nodes_types.get(node_id)

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Node_Id]:      # Get all nodes of a specific type
        return self.data.nodes_by_type.get(node_type.__name__, set())

    def get_nodes_by_type_name(self, type_name: str) -> Set[Node_Id]:                        # Get all nodes by type name string
        return self.data.nodes_by_type.get(type_name, set())

    def get_all_node_types(self) -> Set[str]:                                                # Get all unique node type names
        return set(self.data.nodes_by_type.keys())

    def has_node_type(self, type_name: str) -> bool:                                         # Check if node type exists
        return type_name in self.data.nodes_by_type

    def count_nodes_by_type(self, type_name: str) -> int:                                    # Count nodes of a specific type
        return len(self.data.nodes_by_type.get(type_name, set()))

    # =========================================================================
    # Edge Type - Query Methods
    # =========================================================================

    def get_edge_type(self, edge_id: Edge_Id) -> Optional[str]:                              # Get type name for a specific edge
        return self.data.edges_types.get(edge_id)

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Edge_Id]:      # Get all edges of a specific type
        return self.data.edges_by_type.get(edge_type.__name__, set())

    def get_edges_by_type_name(self, type_name: str) -> Set[Edge_Id]:                        # Get all edges by type name string
        return self.data.edges_by_type.get(type_name, set())

    def get_all_edge_types(self) -> Set[str]:                                                # Get all unique edge type names
        return set(self.data.edges_by_type.keys())

    def has_edge_type(self, type_name: str) -> bool:                                         # Check if edge type exists
        return type_name in self.data.edges_by_type

    def count_edges_by_type(self, type_name: str) -> int:                                    # Count edges of a specific type
        return len(self.data.edges_by_type.get(type_name, set()))

    # =========================================================================
    # Node-Edge Type Query Methods
    # =========================================================================

    def get_node_incoming_edges_by_type(self, node_id  : Node_Id ,                           # Get incoming edges for a node filtered by type
                                              type_name: str
                                         ) -> Set[Edge_Id]:
        return self.data.nodes_to_incoming_edges_by_type.get(node_id, {}).get(type_name, set())

    def get_node_outgoing_edges_by_type(self, node_id  : Node_Id ,                           # Get outgoing edges for a node filtered by type
                                              type_name: str
                                         ) -> Set[Edge_Id]:
        return self.data.nodes_to_outgoing_edges_by_type.get(node_id, {}).get(type_name, set())

    def get_node_edge_types_incoming(self, node_id: Node_Id) -> Set[str]:                    # Get all edge types incoming to a node
        return set(self.data.nodes_to_incoming_edges_by_type.get(node_id, {}).keys())

    def get_node_edge_types_outgoing(self, node_id: Node_Id) -> Set[str]:                    # Get all edge types outgoing from a node
        return set(self.data.nodes_to_outgoing_edges_by_type.get(node_id, {}).keys())

    # =========================================================================
    # Raw Data Accessors
    # =========================================================================

    def nodes_types(self) -> Dict[Node_Id, str]:                                             # Raw accessor for nodes_types
        return self.data.nodes_types

    def nodes_by_type(self) -> Dict[str, Set[Node_Id]]:                                      # Raw accessor for nodes_by_type
        return self.data.nodes_by_type

    def edges_types(self) -> Dict[Edge_Id, str]:                                             # Raw accessor for edges_types
        return self.data.edges_types

    def edges_by_type(self) -> Dict[str, Set[Edge_Id]]:                                      # Raw accessor for edges_by_type
        return self.data.edges_by_type

    def nodes_to_incoming_edges_by_type(self) -> Dict[Node_Id, Dict[str, Set[Edge_Id]]]:     # Raw accessor
        return self.data.nodes_to_incoming_edges_by_type

    def nodes_to_outgoing_edges_by_type(self) -> Dict[Node_Id, Dict[str, Set[Edge_Id]]]:     # Raw accessor
        return self.data.nodes_to_outgoing_edges_by_type