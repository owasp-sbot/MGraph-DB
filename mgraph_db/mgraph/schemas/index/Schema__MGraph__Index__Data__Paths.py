from typing                                                         import Dict, Set
from mgraph_db.mgraph.schemas.identifiers.Edge_Path                 import Edge_Path
from mgraph_db.mgraph.schemas.identifiers.Node_Path                 import Node_Path
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id


class Schema__MGraph__Index__Data__Paths(Type_Safe):
    nodes_by_path: Dict[Node_Path, Set[Node_Id]]                                             # node_path -> set of node_ids
    edges_by_path: Dict[Edge_Path, Set[Edge_Id]]                                             # edge_path -> set of edge_ids