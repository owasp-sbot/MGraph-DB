from typing                                                         import Dict, Set, Tuple
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class Schema__MGraph__Index__Data__Edges(Type_Safe):
    edges_to_nodes         : Dict[Edge_Id, Tuple[Node_Id, Node_Id]]                          # edge_id -> (from_node_id, to_node_id)
    nodes_to_outgoing_edges: Dict[Node_Id, Set[Edge_Id]]                                     # node_id -> set of outgoing edge_ids
    nodes_to_incoming_edges: Dict[Node_Id, Set[Edge_Id]]                                     # node_id -> set of incoming edge_ids