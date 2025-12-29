from typing                                                         import Dict, Set
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id

class Schema__MGraph__Index__Data__Labels(Type_Safe):
    edges_predicates       : Dict[Edge_Id, Safe_Id]                                             # edge_id -> predicate
    edges_by_predicate     : Dict[Safe_Id, Set[Edge_Id]]                                        # predicate -> set of edge_ids
    edges_incoming_labels  : Dict[Edge_Id, Safe_Id]                                             # edge_id -> incoming_label
    edges_by_incoming_label: Dict[Safe_Id, Set[Edge_Id]]                                        # incoming_label -> set of edge_ids
    edges_outgoing_labels  : Dict[Edge_Id, Safe_Id]                                             # edge_id -> outgoing_label
    edges_by_outgoing_label: Dict[Safe_Id, Set[Edge_Id]]                                        # outgoing_label -> set of edge_ids