from typing                                                        import Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id  import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id  import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id  import Safe_Id
from osbot_utils.type_safe.Type_Safe                               import Type_Safe

# todo: see if the types below can be changed from str to type (since Type_Safe now supports it)

class Schema__MGraph__Index__Data(Type_Safe):
    edges_to_nodes                 : Dict[Edge_Id , tuple[Node_Id,  Node_Id ]]  # edge_id -> (from_node_id, to_node_id)
    edges_by_type                  : Dict[str     , set[Edge_Id             ]]  # edge_type -> set of edge_ids
    edges_by_predicate             : Dict[Safe_Id , set[Edge_Id             ]]  # Maps predicate to edge_ids
    edges_by_incoming_label        : Dict[Safe_Id , set[Edge_Id             ]]  # Maps incoming label to edge_ids
    edges_by_outgoing_label        : Dict[Safe_Id , set[Edge_Id             ]]  # Maps outgoing label to edge_ids
    edges_predicates               : Dict[Edge_Id , Safe_Id                  ]  # Maps edge_id to predicate
    edges_types                    : Dict[Edge_Id , str                      ]
    nodes_by_type                  : Dict[str     , set  [Node_Id           ]]  # node_type -> set of node_ids
    nodes_types                    : Dict[Node_Id , str                      ]
    nodes_to_incoming_edges        : Dict[Node_Id , set  [Edge_Id           ]]  # node_id -> set of incoming edge_ids
    nodes_to_incoming_edges_by_type: Dict[Node_Id , Dict [str, set[Edge_Id] ]]
    nodes_to_outgoing_edges        : Dict[Node_Id , set  [Edge_Id           ]]  # node_id -> set of outgoing edge_ids
    nodes_to_outgoing_edges_by_type: Dict[Node_Id , Dict [str, set[Edge_Id] ]]

