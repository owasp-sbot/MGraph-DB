from typing                                                          import Type, Set, Optional, Any
from mgraph_db.mgraph.index.MGraph__Index__Edges                     import MGraph__Index__Edges
from mgraph_db.mgraph.index.MGraph__Index__Labels                    import MGraph__Index__Labels
from mgraph_db.mgraph.index.MGraph__Index__Types                     import MGraph__Index__Types
from mgraph_db.mgraph.index.MGraph__Index__Values                    import MGraph__Index__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                   import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value            import Schema__MGraph__Node__Value
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id    import Safe_Id
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe


class MGraph__Index__Query(Type_Safe):
    edges_index : MGraph__Index__Edges  = None                                                      # Edge-node relationships
    labels_index: MGraph__Index__Labels = None                                                      # Edge labels/predicates
    types_index : MGraph__Index__Types  = None                                                      # Node/edge types
    values_index: MGraph__Index__Values = None                                                      # Value node lookups

    # =========================================================================
    # Value-Based Queries
    # =========================================================================

    def get_nodes_connected_to_value(self, value    : Any                                    ,
                                           edge_type: Type[Schema__MGraph__Edge       ] = None,
                                           node_type: Type[Schema__MGraph__Node__Value] = None
                                      ) -> Set[Node_Id]:
        """Get nodes connected to a value node, optionally filtered by edge type."""
        value_type = type(value)
        if node_type is None:
            node_type = Schema__MGraph__Node__Value

        node_id = self.values_index.get_node_id_by_value(value_type=value_type, value=value, node_type=node_type)
        if not node_id:
            return set()

        incoming_edges = self.edges_index.get_node_id_incoming_edges(node_id)

        if edge_type:
            edge_type_name = edge_type.__name__
            incoming_edges = {e for e in incoming_edges if self.types_index.get_edge_type(e) == edge_type_name}

        return {self.edges_index.get_edge_from_node(e) for e in incoming_edges if self.edges_index.get_edge_from_node(e)}

    # =========================================================================
    # Node Connection Queries
    # =========================================================================

    def get_node_connected_to_node__outgoing(self, node_id: Node_Id, edge_type: str) -> Optional[Node_Id]:
        """Get target node connected via outgoing edge of specific type."""
        connected_edges = self.types_index.get_node_outgoing_edges_by_type(node_id, edge_type)
        if connected_edges:
            edge_id = next(iter(connected_edges))
            return self.edges_index.get_edge_to_node(edge_id)
        return None

    def get_node_connected_to_node__incoming(self, node_id: Node_Id, edge_type: str) -> Optional[Node_Id]:
        """Get source node connected via incoming edge of specific type."""
        connected_edges = self.types_index.get_node_incoming_edges_by_type(node_id, edge_type)
        if connected_edges:
            edge_id = next(iter(connected_edges))
            return self.edges_index.get_edge_from_node(edge_id)
        return None

    # =========================================================================
    # Predicate-Based Queries
    # =========================================================================

    def get_node_outgoing_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id) -> Set[Edge_Id]:
        """Get outgoing edges filtered by predicate."""
        return self.edges_index.get_node_id_outgoing_edges(node_id) & self.labels_index.get_edges_by_predicate(predicate)

    def get_node_incoming_edges_by_predicate(self, node_id: Node_Id, predicate: Safe_Id) -> Set[Edge_Id]:
        """Get incoming edges filtered by predicate."""
        return self.edges_index.get_node_id_incoming_edges(node_id) & self.labels_index.get_edges_by_predicate(predicate)

    def get_nodes_by_predicate(self, from_node_id: Node_Id, predicate: Safe_Id) -> Set[Node_Id]:
        """Get target nodes reachable via predicate from source node."""
        edge_ids = self.get_node_outgoing_edges_by_predicate(from_node_id, predicate)
        return {self.edges_index.get_edge_to_node(e) for e in edge_ids if self.edges_index.get_edge_to_node(e)}

    def get_nodes_by_incoming_predicate(self, to_node_id: Node_Id, predicate: Safe_Id) -> Set[Node_Id]:
        """Get source nodes reachable via predicate to target node."""
        edge_ids = self.get_node_incoming_edges_by_predicate(to_node_id, predicate)
        return {self.edges_index.get_edge_from_node(e) for e in edge_ids if self.edges_index.get_edge_from_node(e)}

    # =========================================================================
    # Type-Based Queries
    # =========================================================================

    def get_nodes_by_outgoing_edge_type(self, node_id: Node_Id, edge_type: str) -> Set[Node_Id]:
        """Get all target nodes reachable via edges of specific type."""
        edge_ids = self.types_index.get_node_outgoing_edges_by_type(node_id, edge_type)
        return {self.edges_index.get_edge_to_node(e) for e in edge_ids if self.edges_index.get_edge_to_node(e)}

    def get_nodes_by_incoming_edge_type(self, node_id: Node_Id, edge_type: str) -> Set[Node_Id]:
        """Get all source nodes reachable via edges of specific type."""
        edge_ids = self.types_index.get_node_incoming_edges_by_type(node_id, edge_type)
        return {self.edges_index.get_edge_from_node(e) for e in edge_ids if self.edges_index.get_edge_from_node(e)}