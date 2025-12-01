from typing                                                         import Dict, Set
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id   import Safe_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Schema__MGraph__Index__Data(Type_Safe):
    edges_by_path                  : Dict[Edge_Path, Set[Edge_Id           ]]  # path -> set of edge_ids
    edges_by_predicate             : Dict[Safe_Id  , Set[Edge_Id           ]]  # predicate -> set of edge_ids
    edges_by_incoming_label        : Dict[Safe_Id  , Set[Edge_Id           ]]  # incoming label -> set of edge_ids
    edges_by_outgoing_label        : Dict[Safe_Id  , Set[Edge_Id           ]]  # outgoing label -> set of edge_ids
    edges_by_type                  : Dict[str      , Set[Edge_Id           ]]  # edge_type name -> set of edge_ids
    edges_predicates               : Dict[Edge_Id  , Safe_Id                ]  # edge_id -> predicate
    edges_to_nodes                 : Dict[Edge_Id  , tuple[Node_Id, Node_Id]]  # edge_id -> (from_node_id, to_node_id)
    edges_types                    : Dict[Edge_Id  , str                    ]  # edge_id -> edge_type name
    nodes_by_path                  : Dict[Node_Path, Set[Node_Id           ]]  # path -> set of node_ids
    nodes_by_type                  : Dict[str      , Set[Node_Id           ]]  # node_type name -> set of node_ids
    nodes_to_incoming_edges        : Dict[Node_Id  , Set[Edge_Id           ]]  # node_id -> set of incoming edge_ids
    nodes_to_incoming_edges_by_type: Dict[Node_Id  , Dict[str, Set[Edge_Id]]]  # node_id -> {edge_type: set of edge_ids}
    nodes_to_outgoing_edges        : Dict[Node_Id  , Set[Edge_Id           ]]  # node_id -> set of outgoing edge_ids
    nodes_to_outgoing_edges_by_type: Dict[Node_Id  , Dict[str, Set[Edge_Id]]]  # node_id -> {edge_type: set of edge_ids}
    nodes_types                    : Dict[Node_Id  , str                    ]  # node_id -> node_type name