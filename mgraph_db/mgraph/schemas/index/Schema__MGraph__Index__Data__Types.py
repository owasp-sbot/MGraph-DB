from typing                                                         import Dict, Set
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Index__Data__Types(Type_Safe):
    nodes_types                    : Dict[Node_Id, str]                                      # node_id -> type_name
    nodes_by_type                  : Dict[str, Set[Node_Id]]                                 # type_name -> set of node_ids
    edges_types                    : Dict[Edge_Id, str]                                      # edge_id -> type_name
    edges_by_type                  : Dict[str, Set[Edge_Id]]                                 # type_name -> set of edge_ids
    nodes_to_incoming_edges_by_type: Dict[Node_Id, Dict[str, Set[Edge_Id]]]                  # node_id -> {type_name -> set of edge_ids}
    nodes_to_outgoing_edges_by_type: Dict[Node_Id, Dict[str, Set[Edge_Id]]]                  # node_id -> {type_name -> set of edge_ids}